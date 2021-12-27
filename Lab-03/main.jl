#!usr/bin/julia

using CSV
using DataFrames
using Random
using Statistics
using ScikitLearn.CrossValidation: train_test_split
println("Include finished")

# For testing only
#=
using DecisionTree
=#

# Calculate Entropy
function entropy(counts, n_samples)
  if n_samples == 0
    return 0
  end

  prob = [i / n_samples for i in counts]
  return -sum(prob .* log.(prob))
end

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

function get_entropy(y_predict, y)
  n = length(y)

#  println(y_predict, y)

  entropy_true, n_true = entropy_of_one_division(y[y_predict])
  entropy_false, n_false = entropy_of_one_division(y[Not(y_predict)])

  s = n_true * entropy_true * 1.0 / n + n_false * entropy_false * 1.0 / n

  return s
end

println("Entropy finished")

struct ID3Tree
  tree::Dict
  depth::Int64
end

function fit(self::ID3Tree, X, y, node = Dict(), depth = 0)
  if all(y == y[1])
    return Dict("val" => y[1])

  else
    col_idx, cutoff, entropy = find_best_split_of_all(self, X, y)

    y_left = y[X[:, col_idx] .< cutoff]
    y_right = y[X[:, col_idx] .>= cutoff]

    node["index_col"] = col_idx
    node["cutoff"] = cutoff
    node["val"] = mean(y)
    node["left"] = fit(X[X[:, col_idx] < cutoff], y_left, Dict(), depth + 1)
    node["right"] = fit(X[X[:, col_idx] >= cutoff], y_right, Dict(), depth + 1)

    self.depth += 1
    self.tree = node

    return node
  end
end

function find_best_split_of_all(self::ID3Tree, X, y)
  col_idx, cutoff = nothing, nothing
  min_entropy = 1

  for i in 1:length(X[1, :])
    println(length(X[:, 1]), i)
    # println(X[:, i])
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

function predict(self::ID3Tree, X)
  tree = self.tree
  pred = zeros(length(X))

  for (i, c) in enumerate(X)
    pred[i] = _predict(self, c)
  end

  return pred
end

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

println("ID3Struct finished")

# Loading dataset
raw_df = DataFrame(CSV.File("iris.csv"))

X = float.(Matrix(raw_df[:, Not("variety")]))
y = raw_df[:, "variety"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3334)

println("Splitted successfully")
println("Training length: $(length(X_train))")
println("Testing legth: $(length(X_test))")

# Running 
model = ID3Tree(Dict(), 0)
tree = fit(model, X_train, y_train)
train_pred = predict(model, X_train)
println("Accuracy of decision tree on training data: $(accuracy_score(y_train, train_pred))")
test_pred = predict(model, X_test)
println("Accuracy of decision tree on testing data: $(accuracy_score(y_test, test_pred))")
#=
# For testing only.
model = DecisionTreeClassifier(max_depth = 2)
fit!(model, X_train, y_train)

print_tree(model, 5)

using ScikitLearn.CrossValidation: cross_val_score

accuracy = cross_val_score(model, X_test, y_test, cv = 3)
=#
