# arcade_payments.py - Single module for all payment logic

import asyncio
from cashu.wallet.wallet import Wallet
from dataclasses import dataclass
import time

@dataclass
class GameSession:
    """Simple in-memory session (no database needed)"""
    credits: int = 0
    invoice: str = ""
    quote_id: str = ""
    amount_sats: int = 0
    ln_address: str = ""  # Optional: for refunds/payouts
    created_at: float = 0
    
# Global state (single player)
current_session = None
wallet = None

MINT_URL = "https://mint.minibits.cash/Bitcoin"
SATS_PER_CREDIT = 100

async def init_wallet():
    """Initialize Cashu wallet once at startup"""
    global wallet
    if wallet is None:
        wallet = await Wallet.with_db(MINT_URL, db="arcade_wallet")
        await wallet.load_mint()
    return wallet

async def create_payment_request(num_credits: int) -> dict:
    """
    Generate Lightning invoice for credits.
    Returns invoice string and QR code data.
    """
    global current_session
    
    await init_wallet()
    amount_sats = num_credits * SATS_PER_CREDIT
    
    # Request Lightning invoice from mint
    mint_quote = await wallet.request_mint(amount_sats)
    
    # Create simple session (no database)
    current_session = GameSession(
        credits=0,
        invoice=mint_quote.request,
        quote_id=mint_quote.quote,
        amount_sats=amount_sats,
        created_at=time.time()
    )
    
    return {
        "invoice": mint_quote.request,
        "amount_sats": amount_sats,
        "num_credits": num_credits
    }

async def check_payment_received() -> tuple[bool, int]:
    """
    Check if invoice was paid. Call this in your game loop.
    Returns (paid: bool, credits: int)
    """
    global current_session
    
    if not current_session:
        return False, 0
    
    if current_session.credits > 0:
        return True, current_session.credits
    
    # Try to mint (will succeed if invoice paid)
    try:
        await wallet.mint(current_session.amount_sats, quote_id=current_session.quote_id)
        current_session.credits = current_session.amount_sats // SATS_PER_CREDIT
        return True, current_session.credits
    except:
        return False, 0

def use_credit() -> int:
    """
    Deduct one credit for a game.
    Returns remaining credits.
    """
    global current_session
    
    if not current_session or current_session.credits < 1:
        raise ValueError("No credits available")
    
    current_session.credits -= 1
    return current_session.credits

async def payout_winnings(amount_sats: int, ln_address: str) -> bool:
    """
    Pay winnings to Lightning address.
    Returns True if successful.
    """
    from routstr.payment.lnurl import raw_send_to_lnurl
    from routstr.wallet import get_proofs_per_mint_and_unit
    
    await init_wallet()
    
    # Get available proofs
    proofs = get_proofs_per_mint_and_unit(wallet, MINT_URL, "sat", not_reserved=True)
    
    # Select proofs for payout
    send_proofs, _ = await wallet.select_to_send(
        proofs, amount_sats, set_reserved=True, include_fees=False
    )
    
    # Send to Lightning address
    try:
        await raw_send_to_lnurl(wallet, send_proofs, ln_address, "sat")
        return True
    except Exception as e:
        print(f"Payout failed: {e}")
        return False

async def payout_winnings_as_token(amount_sats: int) -> str:
    """
    Alternative: Return winnings as Cashu token (show QR code).
    Player scans with their Cashu wallet.
    """
    from routstr.wallet import send_token
    
    await init_wallet()
    token = await send_token(amount_sats, "sat")
    return token

def end_session():
    """Clear current session"""
    global current_session
    current_session = None