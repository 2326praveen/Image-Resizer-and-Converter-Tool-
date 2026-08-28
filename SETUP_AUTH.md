# Optional Login — Setup Guide

This adds **optional** accounts to Image Studio Pro using Supabase
(free tier Postgres + built-in auth). Guests keep full access to every
feature with no persistence, exactly as today. Logged-in users get their
history and settings saved across sessions and devices.

## 1. Create a Supabase project

1. Go to https://supabase.com → New project (free tier).
2. Wait ~2 minutes for provisioning.
3. Go to **Settings → API** and copy:
   - `Project URL`
   - `anon public` key

## 2. Add secrets

**Locally** — create/edit `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOi..."
```

**On Streamlit Community Cloud** — go to your app → Settings → Secrets,
and paste the same two lines. Never commit `secrets.toml` to git; add it
to `.gitignore` if it isn't already there.

## 3. Create the database schema

In Supabase, go to **SQL Editor → New query**, paste and run:

```sql
create table public.profiles (
  id uuid references auth.users(id) primary key,
  username text,
  created_at timestamptz default now()
);

create table public.user_history (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) not null,
  original_name text,
  original_size_kb numeric,
  new_size_kb numeric,
  format text,
  dimensions text,
  compression_pct numeric,
  created_at timestamptz default now()
);

create table public.user_settings (
  user_id uuid references auth.users(id) primary key,
  theme text default 'dark',
  default_format text,
  preferences jsonb default '{}'::jsonb,
  updated_at timestamptz default now()
);

-- Row Level Security: each user can only ever read/write their own rows
alter table public.profiles enable row level security;
alter table public.user_history enable row level security;
alter table public.user_settings enable row level security;

create policy "Users manage own profile" on public.profiles
  for all using (auth.uid() = id);

create policy "Users manage own history" on public.user_history
  for all using (auth.uid() = user_id);

create policy "Users manage own settings" on public.user_settings
  for all using (auth.uid() = user_id);
```

## 4. Install the dependency

Add to `requirements.txt`:

```
supabase
```

## 5. Wire it into app.py

- Copy `utils/auth.py` and `utils/persistence.py` into your `utils/` folder.
- Follow `app_integration_snippet.py` — call `render_auth_sidebar()` once
  near the top of `app.py`, and use `log_conversion()` / `get_display_history()`
  in place of your current direct `st.session_state["history"]` calls.

## 6. Email confirmation (decide now)

By default Supabase requires users to click a confirmation email before
they can log in. For a small side project this is often more friction
than it's worth:

- **Keep it on** (recommended if you'll have real public users) — no
  changes needed.
- **Turn it off** (faster to demo/test) — Supabase dashboard →
  Authentication → Providers → Email → toggle off "Confirm email".

## Known limitations to be upfront about

- **Free tier pauses after 7 days of inactivity.** The project auto-resumes
  on the next request but that first request will be slow (~a few
  seconds). Fine for a personal/demo project; worth knowing if you cite
  this in an interview.
- **Free tier caps:** 500MB database, 50,000 monthly active users — far
  more than a side project needs, but good to know the ceiling exists.
- Guests are completely unaffected by any of this — no login prompt is
  required to use the app, and nothing here changes existing behavior for
  them.
