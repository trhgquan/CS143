#!usr/bin/julia

using CSV
using DataFrames
using Random

# Split dataframe into parts with percentage.
# Kudos to Bogumił Kamiński - https://stackoverflow.com/a/66059719
function splitdf(df, pct)
  @assert 0 <= pct <= 1

  ids = collect(axes(df, 1))

  shuffle!(ids)

  sel = ids .<= nrow(df) .* pct

  return view(df, sel, :), view(df, .!sel, :)
end

# Loading dataset
raw_df = DataFrame(CSV.File("iris.csv"))

# Split dataset to training (80%) and testing (20%)
splitdf(raw_df, 0.8)
