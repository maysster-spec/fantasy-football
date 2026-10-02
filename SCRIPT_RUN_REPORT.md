# Script run report, 2 Oct 2026

Every `.py` under `Scripts/` was run once in a Linux cloud container on an unmodified copy of the `upload` release tree. No arguments were passed, stdin was closed, and each run was capped at 90 s. Scripts that only stopped for lack of arguments were re-run with safe read-only arguments, and slow ones were re-run with 15 minutes. No script was changed. pandas, numpy and scipy were pip-installed first.

**Cause key:**
- **Blocked website:** the environment's proxy refused the host (CONNECT 403).
- **Missing login/key:** ESPN cookies were needed and not given.
- **Missing data file:** the file is absent, sits at an old sandbox or Windows path, or is out of step with another file.
- **Other:** stated in the row.

**Totals:** runs 89, Missing data file 75, not run 17, Blocked website 13, check reported findings 9, Other 8, Missing login/key 2

| script | result | cause type | detail |
|---|---|---|---|
| `Espn_league_score-draft_2021_2024.py` | fails | Other | Python package `espn_api` not installed; behind it, lm-api-reads.fantasy.espn.com is blocked and cookies are blank |
| `Espn_pull_projections.py` | fails | Blocked website | lm-api-reads.fantasy.espn.com refused by proxy (403); cookies also blank in the upload |
| `after_pull.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `anchor_study.py` | fails | Missing data file | Source\nfl\w2020.csv not in the upload |
| `apply_news.py` | runs |  |  |
| `apply_research.py` | fails | Missing data file | Scripts\gemini_findings.csv not in the upload |
| `board_audit.py` | runs, check FAILS | Other | draft board: 482 rows not 480, 10 of 12 keepers resolve |
| `buf_bias.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../draft_history_2021_2025.csv |
| `build_news.py` | fails | Blocked website | ESPN news host refused by proxy (403); refuses to write a partial file |
| `check_adp_vintage.py` | runs |  |  |
| `check_citations.py` | runs |  |  |
| `check_guards.py` | runs, check FAILS | Other | real finding: defects with no guard (docs 416, 424); notes two checks already failing |
| `check_inputs.py` | runs, check FAILS | Other | real finding: 3 RedZone CSVs read but unused by sheet_engine |
| `check_kit.py` | fails | Missing data file | checks hardcoded G:\ and C:\ folders; all missing here |
| `check_locals.py` | runs |  |  |
| `check_page_logic.py` | runs, check FAILS | Other | real finding on uploaded WEEK_SHEET.html: offers an IR man as a drop |
| `check_page_rules.py` | runs, check FAILS | Other | real finding: WEEK_SHEET.html still prints retracted 6.1% and 11.2% |
| `check_pages.py` | runs, check FAILS | Other | real finding: 1 page shows a template, dead link or missing value |
| `check_plain.py` | runs, check FAILS | Other | real finding: doc-voice (e.g. VBD) on draft-era printed pages |
| `check_sources.py` | runs |  |  |
| `check_vintage.py` | runs |  |  |
| `claim_order_log.py` | fails | Blocked website | lm-api-reads.fantasy.espn.com refused by proxy (403) |
| `code_rebuild_spine_v5.py` | fails | Missing data file | reads src\code_universe.csv relative to cwd; not present |
| `context_audit.py` | runs |  |  |
| `cookie_jar.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `cookie_jar.py` | fails | Missing login/key | interactive: wants to pip-install browser_cookie3 and paste ESPN cookies |
| `delta_gaps.py` | runs |  |  |
| `depth_map.py` | runs |  |  |
| `done.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `done.py` | runs |  |  |
| `draft_night.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `env_study.py` | fails | Missing data file | Source\nfl\w2022.csv not in the upload |
| `espn_api_python_script_historical_trans.py` | fails | Other | Python package `espn_api` not installed; behind it, lm-api-reads.fantasy.espn.com is blocked and cookies are blank |
| `espn_draft_injector_Gemini.py` | not run | Other | POSTs a prerank to ESPN with no dry run; ESPN writes are Matt's only (directive 0.4) |
| `espn_historical_scores.py` | fails | Blocked website | lm-api-reads.fantasy.espn.com refused by proxy (403) |
| `fetch_keepers.py` | fails | Blocked website | needs --dry/--write/--probe; with --dry, lm-api-reads.fantasy.espn.com refused (403) |
| `ff.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `gameday.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `homer_bias.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../draft_history_2021_2025.csv |
| `import_injury_sweep.py` | fails | Missing data file | needs a Gemini sweep CSV argument; none in the upload (injurysheet holds only an .xlsx) |
| `keeper_swap.py` | runs |  | needs --check or --write; ran clean with --check |
| `lineup.py` | fails | Blocked website | lm-api-reads.fantasy.espn.com refused by proxy (403) |
| `lineups.py` | fails | Blocked website | lm-api-reads.fantasy.espn.com refused by proxy (403); no lineups returned |
| `lookahead_box.py` | runs |  |  |
| `make_board.py` | runs |  |  |
| `make_board_file.py` | fails | Missing data file | draft-era spine out of step: 2 of 12 keepers (Aubrey, Buccaneers D/ST) unmatched |
| `make_commands.py` | runs |  |  |
| `make_fallback.py` | runs |  |  |
| `make_gridboard.py` | partial | Other | HTML written; no PDF renderer (Chrome/Edge/wkhtmltopdf) here |
| `make_howto.py` | runs |  |  |
| `make_online.py` | runs |  |  |
| `make_prerank.py` | runs |  |  |
| `make_sheets.py` | partial | Other | wkhtmltopdf not installed; 0 of 3 PDFs |
| `make_shortcuts.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `make_shortcuts.py` | fails | Other | no Windows Desktop folder (Windows-only by design) |
| `make_tiers.py` | partial | Other | HTML written; no PDF renderer here |
| `mark_rookies.py` | fails | Missing data file | games_2025.csv does not cover the whole board; refuses |
| `mkoverride.py` | runs |  |  |
| `mkvalue.py` | runs |  |  |
| `my_take.py` | runs |  |  |
| `ol_study.py` | fails | Missing data file | Source\nfl\w2020.csv not in the upload |
| `parse_ladder.py` | runs |  |  |
| `parse_takes.py` | runs |  | needs files; ran clean on ..\10_Gemni\*.md |
| `probe_stats_payload.py` | fails | Blocked website | lm-api-reads.fantasy.espn.com refused by proxy (403) |
| `proj_due.py` | runs |  |  |
| `reach_study.py` | fails | Missing data file | old sandbox path /home/claude/nfl/w2021.csv |
| `refresh_adp.py` | runs |  |  |
| `refresh_proj.py` | runs |  |  |
| `refresh_pull.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `rehearsal.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `rehearsal.py` | runs |  | needs about 10 minutes; completed when given 15 |
| `sept5_after.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `sept5_check.py` | runs |  |  |
| `set_cookies.py` | fails | Missing login/key | prompts for ESPN SWID and espn_s2; none supplied |
| `setup_tasks.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `setup_tasks.ps1` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `setup_tasks_simple.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `sheet_engine.py` | runs |  |  |
| `smoke_spine.py` | fails | Missing data file | hardcoded G:\My Drive\_Fantasy\2026\Scripts path |
| `snaps_2026.py` | runs |  |  |
| `spot.py` | runs |  | needs a player name; ran clean with "Puka Nacua" |
| `sync_desk_copies.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `sync_desk_copies.py` | fails | Missing data file | copies from hardcoded G:\...\Source\*.pdf; not present |
| `tidy_docs.py` | runs |  |  |
| `tidy_duplicates.py` | fails | Missing data file | hardcoded G:\My Drive\_Fantasy\2026\Source path |
| `to_pdf.py` | fails | Other | no PDF renderer here; reports draft PDFs out of date |
| `todo_page.py` | runs |  |  |
| `values.py` | fails | Missing data file | rankers.csv no longer exists; old /home/claude paths |
| `verify_prerank.py` | fails | Missing data file | hardcoded G:\ path to ESPN_prerank_with_ids.csv (file exists in live_draft\) |
| `waiver_study.py` | fails | Missing data file | 0 of 1,230 adds resolve to the weekly stat file, then crashes on an empty frame |
| `waivers.py` | fails (exit 0) | Blocked website | lm-api-reads.fantasy.espn.com refused on every week; writes empty reports and exits 0 |
| `weekend_check.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `weekend_check.py` | fails | Blocked website | lm-api-reads.fantasy.espn.com refused; also checks G:\ and C:\ folders that do not exist here |
| `weekly.bat` | not run | Other | Windows batch/PowerShell; no cmd.exe here. Each .py it calls is tested on its own row |
| `width_study.py` | runs |  |  |
| `wire.py` | fails | Blocked website | local files load fine; lm-api-reads.fantasy.espn.com refused (403), exits 2 silently |
| `live_draft/bench_lineup.py` | runs |  |  |
| `live_draft/bridge_server.py` | runs |  | local server on 127.0.0.1:8787, stopped at 90s (runs until Ctrl+C) |
| `live_draft/code_live_engine.py` | runs |  |  |
| `live_draft/live_draft.py` | fails | Blocked website | polls lm-api-reads.fantasy.espn.com, every poll refused; loops until stopped |
| `live_draft/probe_sources.py` | fails | Blocked website | needs --league; then every ESPN host incl. lm-api-writes refused; loops |
| `research/adp_registry_from_fp.py` | runs |  | needs --year/--file; ran clean with --check-avg |
| `research/audit_desk.py` | runs |  |  |
| `research/audit_directive.py` | runs |  |  |
| `research/bars.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../byes_2026.csv |
| `research/blend_weight.py` | runs |  |  |
| `research/build_dst.py` | runs |  |  |
| `research/build_inherit.py` | runs |  |  |
| `research/build_page.py` | fails | Missing data file | sheet.json not present (old sandbox output) |
| `research/build_pedigree.py` | runs |  |  |
| `research/career_ceiling_gate_KILLED.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../_nflverse_cache (file exists in the real cache) |
| `research/cascade.py` | fails | Missing data file | old sandbox folder /home/claude/work/lb/new |
| `research/claim_rank.py` | runs |  |  |
| `research/clear_path.py` | fails | Missing data file | player_stats_2022.csv (old nflverse name) not present |
| `research/close_check.py` | runs |  |  |
| `research/dst_all.py` | fails | Missing data file | play_by_play_2021.csv.gz expected in research\ (copy is in _nflverse_cache) |
| `research/dst_k_supply.py` | runs |  |  |
| `research/dst_waivers.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../espn_projections_2026_20260907_1258.csv |
| `research/efficiency_check.py` | fails | Missing data file | advstats_week_rush_2022.csv not present |
| `research/emergence_by_tier.py` | fails | Missing data file | player_stats_2021.csv (old nflverse name) not present |
| `research/emergence_lead.py` | fails | Missing data file | player_stats_2021.csv not present |
| `research/emphasis.py` | fails | Missing data file | old sandbox folder /home/claude/work/kit |
| `research/gofcheck.py` | fails | Missing data file | old sandbox folder /home/claude/work/kit |
| `research/injury_overlap.py` | fails | Missing data file | player_stats_2021.csv not present |
| `research/job_slope.py` | runs |  |  |
| `research/k12_replacement.py` | runs |  |  |
| `research/kick.py` | fails | Missing data file | old sandbox path /home/claude/k_weekly_2021_2025.csv |
| `research/lane_precision.py` | fails | Missing data file | player_stats_2021.csv not present |
| `research/matchup_term.py` | runs |  |  |
| `research/moves.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../byes_2026.csv |
| `research/multi.py` | fails | Missing data file | old sandbox folder /home/claude/work/lb/new |
| `research/open_threads.py` | runs |  |  |
| `research/own_quality_dst.py` | fails | Missing data file | Source\dst_weekly_2021_2025.csv lacks the pts_adj column it expects |
| `research/own_quality_dst2.py` | fails | Missing data file | Source\dst_weekly_2021_2025.csv lacks the pts_adj column it expects |
| `research/pairs.py` | runs |  |  |
| `research/playoff_odds.py` | runs |  |  |
| `research/potential.py` | fails | Missing data file | draft_picks.csv not present |
| `research/potential_value.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../byes_2026.csv |
| `research/price_dst_k_terms.py` | runs |  |  |
| `research/qb2_window.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../_nflverse_cache (file exists in the real cache) |
| `research/qb_matchup.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../_nflverse_cache (file exists in the real cache) |
| `research/qb_pair_playoffs.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../_nflverse_cache (file exists in the real cache) |
| `research/reach_threshold.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../_nflverse_cache (file exists in the real cache) |
| `research/reprice.py` | fails | Missing data file | old sandbox path /home/claude/work/lb/new/board_v8_fixed.csv |
| `research/rival_need.py` | runs |  |  |
| `research/scarcity.py` | fails | Missing data file | old sandbox path /home/claude/dst/games.csv |
| `research/seat_weeks.py` | runs |  |  |
| `research/sheetdata.py` | fails | Missing data file | old sandbox path /mnt/user-data/.../byes_2026.csv |
| `research/shoot.py` | fails | Missing data file | old sandbox folder /home/claude/work/kit |
| `research/slate.py` | runs |  |  |
| `research/te_pair.py` | runs |  |  |
| `research/tired.py` | fails | Missing data file | play_by_play_2023.csv.gz expected in research\ (copy is in _nflverse_cache) |
| `research/tired2.py` | fails | Missing data file | tired_games.csv (output of tired.py) not present |
| `research/usage_jump_by_tier.py` | fails | Missing data file | player_stats_2021.csv not present |
| `research/vegas_streams.py` | runs |  |  |
| `research/wr_pair.py` | runs |  |  |
| `research/a1/a1_injury_sim.py` | fails | Other | imports sheet_engine but does not put Scripts\ on the path from a1\ |
| `research/a1/absence_rates.py` | fails | Missing data file | stats_player_week_2021.csv expected in a1\ (copy is in _nflverse_cache); set A1_DATA |
| `research/b1/b1_absence_bar.py` | fails | Missing data file | 1 rostered man has no row in the projections file |
| `research/b2/b2_depth_order.py` | runs |  |  |
| `research/f1/squeeze.py` | fails | Missing data file | stats_player_week_*.csv expected in f1\ (set F1_DATA to the cache) |
| `research/f1/squeeze_redteam.py` | fails | Missing data file | finds no stats_player_week files in f1\, so no seasons |
| `research/f2/screen_free_wr.py` | fails | Missing data file | no Source\WIRE_*.csv in the upload |
| `research/ir/claim_order_null.py` | runs |  |  |
| `research/ir/ir_return_rate.py` | fails | Missing data file | inj_<season>.csv not present (cache has injuries_<season>.csv) |
| `research/ir/ir_seat_validity.py` | fails | Missing data file | inj_2021.csv not present (cache has injuries_2021.csv) |
| `research/j1/j1_one_currency.py` | fails | Missing data file | 1 rostered man has no row in the projections file |
| `research/j2/j2_bands_2021.py` | runs |  |  |
| `research/j2/j2_seat_odds_matrix.py` | fails | Missing data file | 1 rostered man has no row in the projections file |
| `research/j2/j2_share_and_rate.py` | runs |  |  |
| `research/j3/j3_breadth.py` | runs |  |  |
| `research/j3/j3_product.py` | runs |  |  |
| `research/j4/j4_band_loo.py` | runs |  |  |
| `research/j4/j4_riser_keeper.py` | runs |  |  |
| `research/late_picks/build_weekly.py` | fails | Missing data file | snap_counts_2014.csv (2014 to 2020 not in cache) |
| `research/late_picks/combo.py` | fails | Missing data file | flips.pkl (output of flips.py) not present |
| `research/late_picks/common.py` | runs |  |  |
| `research/late_picks/flips.py` | fails | Missing data file | weekly.pkl (output of build_weekly.py) not present |
| `research/late_picks/hubbard.py` | fails | Missing data file | draft_picks_all.csv not present |
| `research/late_picks/keep_role.py` | fails | Missing data file | weekly.pkl not present |
| `research/late_picks/keep_role_checks.py` | fails | Missing data file | keep_role_backup_2015_2025.pkl not present |
| `research/late_picks/keep_role_variants.py` | fails | Missing data file | weekly.pkl not present |
| `research/late_picks/keep_role_window.py` | fails | Missing data file | keep_role_work_2015_2025.pkl not present |
| `research/late_picks/openings.py` | fails | Missing data file | weekly.pkl not present |
| `research/late_picks/risers.py` | fails | Missing data file | weekly.pkl not present |
| `research/redteam/ctl_307.py` | runs, check FAILS | Other | 86 of 265 player_context rows do not reproduce |
| `research/redteam/redteam_controls.py` | runs, check FAILS | Other | 57 of 65 controls pass; C20 and C24 fail on week sheet |
| `research/rt344/rt1_zero_filers.py` | runs |  |  |
| `research/rt344/rt2_ladder.py` | runs |  |  |
| `research/rt344/rt3_floor.py` | runs |  | needs over 90s; completed when given 15 minutes |
| `research/rt344/rt5_relief.py` | runs |  |  |
| `research/wk1/build_depth_daily.py` | runs |  |  |
| `research/wk1/build_form.py` | runs |  |  |
| `research/wk1/build_lines.py` | runs |  |  |
| `research/wk1/delta_screen.py` | runs |  |  |
| `research/wk1/depth_diff.py` | runs |  |  |
| `research/wk1/job_opens.py` | runs |  |  |
| `research/wk1/practice_out.py` | runs |  |  |
| `research/wk1/rb_composite.py` | fails | Missing data file | stats_player_week_2020.csv not present (cache starts 2021) |
| `research/wk1/reach_gate_test.py` | runs |  |  |
| `research/wk1/redzone_test.py` | runs |  |  |
| `research/wk1/rise_horizon.py` | runs |  |  |
| `research/wk1/rookie_screen.py` | runs |  |  |
| `research/wk1/routes_vs_snaps.py` | runs |  |  |
| `research/wk1/tail_tickets.py` | runs |  |  |
| `research/wk1/te2_split.py` | fails | Missing data file | stats_player_week_2021.csv expected in wk1\ (copy in cache) |
| `research/wk1/week1_share.py` | fails | Missing data file | stats_player_week_*.csv expected in wk1\ (copy in cache) |
| `research/wk1/wk1_redteam.py` | fails | Missing data file | finds no weekly stats in wk1\, so an empty correlation crashes |
| `research/wk1/wk1_redteam2.py` | runs |  |  |
| `research/wk1/wk1_wr_composite.py` | fails | Missing data file | stats_player_week_2021.csv expected in wk1\ (copy in cache) |
| `research/wk1/wopr_spike.py` | runs |  |  |
| `research/wk1/wr_week1_share.py` | fails | Missing data file | stats_player_week_*.csv expected in wk1\ (copy in cache) |
| `research/wk1/xfp_backtest.py` | runs |  |  |
