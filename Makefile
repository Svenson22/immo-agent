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

# Filter
.PHONY: filter-all
filter-all:
	python -m src.filter.run_filter_4a --in-dir data/staged/split --out-dir data/staged/filtered

# Optioneel: taalfilter NL/FR activeren
.PHONY: filter-all-nlfr
filter-all-nlfr:
	python -m src.filter.run_filter_4a --in-dir data/staged/split --out-dir data/staged/filtered --allowed-langs nl,fr

# Per dagbestand (als je per dag wil draaien)
.PHONY: filter-day
filter-day:
	python -m src.filter.run_filter_4a --in-dir data/staged/split --out-dir data/staged/filtered