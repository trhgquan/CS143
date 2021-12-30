#!usr/bin/julia

using DelimitedFiles
using Random
using Statistics

# Calculate Entropy based on probabilities list.
# Input:
#   - counts: list of each sample's appearences.
#   - n_samples: total samples
# Output:
#   - Entropy of that list.
function entropy(counts, n_samples)
  if n_samples == 0
    return 0
  end

  prob = [i / n_samples for i in counts]
  return -sum(prob .* log2.(prob))
end

# Calculate entropy of a divided data group.
# Input:
#   - division: list of items after splitted
# Output:
#   - entropy of list of items
#   - total samples
function entropy_of_one_division(division)
  n_samples = length(division)
  n_classes = Set(division)

  count = []

  for s in n_classes
    temp_count = 0
    
    for i in 1:n_samples
      if division[i] == s
        temp_count += 1
      end
    end

    push!(count, temp_count)
  end

  return entropy(count, n_samples), n_samples
end

# Calculate entropy of a data split
# Input:
#   - y_predict: split decision by cutoff.
#   - y: label vector
# Output:
#   - entropy of the split.
function get_entropy(y_predict, y)
  n = length(y)

  entropy_true, n_true = entropy_of_one_division(y[y_predict])
  entropy_false, n_false = entropy_of_one_division(y[.!(y_predict)])

  s = n_true * entropy_true * 1.0 / n + n_false * entropy_false * 1.0 / n

  return s
end

# ID3 Tree struct
mutable struct ID3Tree
  tree::Dict
  depth::Int64
end

# Fit a model.
# Input:
#   - X: training data
#   - y: training labels
# Output:
#   - A tree node.
function fit(self::ID3Tree, X, y, node = Dict(), depth = 0)
  if all(y .== y[1])
    return Dict("val" => y[1])

  else
    col_idx, cutoff, entropy = find_best_split_of_all(self, X, y)

    y_left = y[X[:, col_idx] .< cutoff]
    y_right = y[X[:, col_idx] .>= cutoff]

    node["index_col"] = col_idx
    node["cutoff"] = cutoff
    node["val"] = mean(y)

    node["left"] = fit(self, X[X[:, col_idx] .< cutoff, :], y_left, Dict(), depth + 1)
    node["right"] = fit(self, X[X[:, col_idx] .>= cutoff, :], y_right, Dict(), depth + 1)

    self.depth += 1
    self.tree = node

    return node
  end
end

# Find best split over all data.
# Input:
#   - X: Data
#   - y: Labels
# Output:
#   - col_idx: id of column having best split.
#   - cutoff: cutoff value
#   - min_entropy: entropy of that split.
function find_best_split_of_all(self::ID3Tree, X, y)
  col_idx, cutoff = nothing, nothing
  min_entropy = 1

  for i in 1:length(X[1, :])
    entropy, cur_cutoff = find_best_split(self, X[:, i], y)
  
    if entropy == 0
      return i, cur_cutoff, entropy
    end

    if entropy <= min_entropy
      min_entropy = entropy
      col_idx = i
      cutoff = cur_cutoff
    end
  end

  return col_idx, cutoff, min_entropy
end

# Find best split over a column
# Input:
#   - col_data: column data
#   - y: labels
# Output:
#   - min_entropy: entropy of best split on that column
#   - cutoff: cutoff value of that column
function find_best_split(self::ID3Tree, col_data, y)
  min_entropy = 10
  cutoff = nothing

  for value in Set(col_data)
    y_predict = col_data .< value

    my_entropy = get_entropy(y_predict, y)

    if my_entropy <= min_entropy
      min_entropy = my_entropy
      cutoff = value
    end
  end

  return min_entropy, cutoff
end

# Predict on a data.
# Input:
#   - X: data
# Output:
#   - pred: predicted labels
function predict(self::ID3Tree, X)
  tree = self.tree
  pred = zeros(length(X[:, 1]))
  
  for i in 1:length(X[:, 1])
    pred[i] = _predict(self, X[i, :])
  end

  return pred
end

# Predict a data row
# Input:
#   - row: data row.
# Output:
#   - predicted label.
function _predict(self::ID3Tree, row)
  cur_layer = self.tree

  while true
    if get(cur_layer, "cutoff", false) == false
      return cur_layer["val"]
    else
      if row[cur_layer["index_col"]] < cur_layer["cutoff"]
        cur_layer = cur_layer["left"]
      else
        cur_layer = cur_layer["right"]
      end
    end
  end
end

# Calculate accuracy score of a predict
# Input:
#   - y_predict: list of predicted labels
#   - y_test: list of correct labels
# Output:
#   - Accuracy score
function accuracy_score(y_predict, y_test)
  correct = 0
  total_samples = length(y_predict)

  for i in 1:total_samples
    if y_predict[i] == y_test[i]
      correct += 1
    end
  end

  return correct * 1.0 / total_samples
end

# Reading raw_df from csv file.
# Input:
#   - filename: csv file name.
# Output:
#   - Matrix consists of string values.
function read_raw_df(filename)
  df = readdlm(filename, ',', String, '\n')

  # Ignore the column name
  raw_df = df[2:end, :]

  return raw_df
end

# Split dataframe to train and test, with test_size
# Input:
#   - df: dataframe to split
#   - test_size: test dataset size
#   - random_state: random seed.
# Output:
#   - Splitted train and test.
#
# Source: https://stackoverflow.com/a/66059719
function train_test_split(df; test_size, random_state = nothing)
  if !isnothing(random_state)
    Random.seed!(random_state)
  end

  @assert 0 <= test_size <= 1

  train_size = 1 - test_size

  ids = collect(axes(df, 1))
  
  # Shuffle the matrix
  df = df[shuffle(1:end), :]

  # Select training and testing dataset.
  sel = ids .<= length(df[:, 1]) .* train_size

  return df[sel, :], df[.!sel, :]
end

# Split a raw dataframe to X (data) and y (label)
# Input:
#   - raw: raw dataframe
# Output:
#   - X: data
#   - y: labels
function create_data_label(raw)
  X = parse.(Float64, raw[:, 1:4])

  y = []
  for s in raw[:, 5]
    if s == "Setosa"
      push!(y, 0)
    end

    if s == "Versicolor"
      push!(y, 1)
    end

    if s == "Virginica"
      push!(y, 2)
    end
  end

  return X, y
end

# Loading dataset
raw_df = read_raw_df("iris.csv")

# Split dataset intro training (2/3) and testing (1/3)
raw_train, raw_test = train_test_split(raw_df, test_size = 0.33, random_state = 42)

# Create training & testing data based on raw data.
X_train, y_train = create_data_label(raw_train)
X_test, y_test = create_data_label(raw_test)

println("Training dataset size: $(length(y_train))")
println("Testing dataset size: $(length(y_test))")

# Create a model and fitting it with training data.
model = ID3Tree(Dict(), 0)
tree = fit(model, X_train, y_train)
train_pred = predict(model, X_train)
println("Accuracy of decision tree on training data: $(accuracy_score(y_train, train_pred))")

# Running predictions on testing data to give testing accuracy.
test_pred = predict(model, X_test)
println("Accuracy of decision tree on testing data: $(accuracy_score(y_test, test_pred))")
