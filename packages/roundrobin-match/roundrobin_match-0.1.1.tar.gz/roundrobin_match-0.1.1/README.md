# roundrobin_match

A CLI library for creating 1on1 and game match schedules.
It uses round robin matching algorithm for python3.

## requirement
- `python3.10 >=`

## install
```bash
pip install roundrobin_match
```

## usage
```bash
# if you do not pass the seed, the result is not shuffled.
roundrobin_match --seed 40 --list alice bob dave
| DAY | alice | bob | dave | break |
| ---- | -------|-----|------|-------|
| 0 | dave | break | alice | bob|
| 1 | break | dave | bob | alice|
| 2 | bob | alice | break | dave|
```

## contribute
- If you want to fix, or add the function, please feel free to submit a PR.