#!usr/bin/julia

using CSV
using DataFrames
using Random

# For testing only
#=
using DecisionTree
=#

# Split dataframe into parts with percentage.
# Kudos to Bogumił Kamiński - https://stackoverflow.com/a/66059719
function splitdf(df, pct)
  @assert 0 <= pct <= 1

  ids = collect(axes(df, 1))

  shuffle!(ids)

  sel = ids .<= nrow(df) .* pct

  return view(df, sel, :), view(df, .!sel, :)
end

# Calculate Entropy
function entropy(freq::Array)
  # Calculate sum of non-zeroes freq only.
  freq_0 = filter(x -> x != 0, freq)
  prob_0 = freq_0 / float.(sum(freq_0))

  # Calculate entropy = -sum(prob_i * log(prob_i))
  return -sum(prob_0 .* log.(prob_0))
end

# Loading dataset
raw_df = DataFrame(CSV.File("iris.csv"))

# Split dataset to training (2/3) and testing (1/3)
train_df, test_df = splitdf(raw_df, 0.666666667)

X_train, X_test = train_df[!, Not("variety")], test_df[!, Not("variety")]
y_train, y_test = train_df[!, "variety"], test_df[!, "variety"]

X_train, X_test = float.(Matrix(X_train)), float.(Matrix(X_test))
y_train, y_test = string.(y_train), string.(y_test)

#=
# For testing only.
model = DecisionTreeClassifier(max_depth = 2)
fit!(model, X_train, y_train)

print_tree(model, 5)

using ScikitLearn.CrossValidation: cross_val_score

accuracy = cross_val_score(model, X_test, y_test, cv = 3)
=#
