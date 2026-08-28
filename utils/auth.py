"""
Optional user authentication for Image Studio Pro, backed by Supabase.

Guests can use every feature of the app without ever touching this module.
Logging in is purely additive: it unlocks persistence of history/settings
across sessions and devices.

Setup required before this works:
  1. Create a free project at https://supabase.com
  2. Add SUPABASE_URL and SUPABASE_ANON_KEY to .streamlit/secrets.toml
     (locally) or to your app's Secrets in Streamlit Community Cloud.
  3. Run the SQL in SETUP_AUTH.md against your Supabase project.
  4. Add `supabase` to requirements.txt.
"""

import streamlit as st

# ── Windows SSL fix: patch the exact gotrue call site ───────────────────────
# Root cause: SyncGoTrueBaseAPI.__init__ (supabase-auth) creates:
#   httpx.Client(verify=True, ...)   ← True = system cert store = broken on Windows
# Since 'verify' IS explicitly in kwargs, a generic httpx.Client patch won't
# intercept it.  We patch SyncGoTrueBaseAPI.__init__ directly to swap
# verify=True → verify=certifi.where() before the httpx.Client is created.
try:
    import certifi
    _certifi_bundle = certifi.where()

    from supabase_auth._sync.gotrue_base_api import SyncGoTrueBaseAPI
    _orig_sync_init = SyncGoTrueBaseAPI.__init__

    def _patched_sync_init(self, *, url, headers, http_client, verify=True, proxy=None):
        # Replace bare True with the certifi CA bundle path
        if verify is True:
            verify = _certifi_bundle
        _orig_sync_init(
            self, url=url, headers=headers,
            http_client=http_client, verify=verify, proxy=proxy,
        )

    SyncGoTrueBaseAPI.__init__ = _patched_sync_init

    # Also patch async variant for completeness
    from supabase_auth._async.gotrue_base_api import AsyncGoTrueBaseAPI
    _orig_async_init = AsyncGoTrueBaseAPI.__init__

    def _patched_async_init(self, *, url, headers, http_client, verify=True, proxy=None):
        if verify is True:
            verify = _certifi_bundle
        _orig_async_init(
            self, url=url, headers=headers,
            http_client=http_client, verify=verify, proxy=proxy,
        )

    AsyncGoTrueBaseAPI.__init__ = _patched_async_init

except Exception:
    pass  # If supabase_auth is not installed, continue without patching


# Guarded auth availability — requires both the supabase package and configured secrets
AUTH_AVAILABLE = False
try:
    from supabase import create_client, Client  # noqa: F401
    if hasattr(st, "secrets") and "SUPABASE_URL" in st.secrets and "SUPABASE_ANON_KEY" in st.secrets:
        AUTH_AVAILABLE = True
except Exception:
    AUTH_AVAILABLE = False


@st.cache_resource
def get_supabase_client() -> "Client":
    """Create (once per process) the Supabase client from secrets.

    SSL is already handled globally by the certifi patch above, so a plain
    create_client() call works correctly on Windows.
    """
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


def sign_up(email: str, password: str, username: str):
    """Create a new account. Returns (success: bool, message: str)."""
    if not email or not password or not username:
        return False, "Please fill in all fields."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    supabase = get_supabase_client()
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"username": username}},
        })
        if res.user:
            # Profile row is created automatically by the handle_new_user
            # trigger (SECURITY DEFINER) on auth.users — no client-side insert.
            if res.session:
                return True, "Account created and signed in."
            return True, "Account created. Check your email to confirm, then log in."
        return False, "Sign up failed. Please try again."
    except Exception as e:
        return False, f"Sign up error: {e}"


def sign_in(email: str, password: str):
    """Log in an existing user. Returns (success: bool, message: str)."""
    if not email or not password:
        return False, "Please enter email and password."

    supabase = get_supabase_client()
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if res.user and res.session:
            st.session_state["user"] = {
                "id": res.user.id,
                "email": res.user.email,
            }
            st.session_state["access_token"] = res.session.access_token
            return True, "Signed in."
        return False, "Invalid email or password."
    except Exception as e:
        return False, f"Login error: {e}"


def sign_out():
    """Log the current user out and clear their session."""
    supabase = get_supabase_client()
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    for key in ("user", "access_token"):
        st.session_state.pop(key, None)


def get_current_user():
    """Return the logged-in user's {id, email} dict, or None if a guest."""
    return st.session_state.get("user")


def is_logged_in() -> bool:
    return "user" in st.session_state
