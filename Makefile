# Run step 3a (split multi-property emails into individual records) for one day
split-day:
	python -m src.split.run_split_3a --in data/raw/$(DAY).jsonl --out-dir data/staged/split

# Run step 3a for all files in data/raw/
split-all:
	for f in data/raw/*.jsonl; do \
		python -m src.split.run_split_3a --in $$f --out-dir data/staged/split; \
	done

# Run step 3a for a specific input file
split:
	python -m src.split.run_split_3a --in $(IN) --out-dir data/staged/split