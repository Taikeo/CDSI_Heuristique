defmodule Heuristique do
  @moduledoc """
  Documentation for `Heuristique`.
  """

  @doc """
  Build a list from the input text file
 
  ## Examples
 
      iex> Metaheuristique.build_list("100M5_1.txt")
      [100, 5, 504]
 
  """
  def build_list() do
    if {:ok, text} = File.read("Instances/100M5_1.txt") do
      String.replace(text, ["\n", "\r"], "")
      |> String.replace(~r/ +/, " ")
      |> String.trim()
      |> String.split(" ")
      |> Enum.map(&String.to_integer/1)
    else
      {:error, "Erreur lors de la lecture du fichier"}
    end
  end

  @doc """
  Get all data from the list build from the text file
 
  ## Examples
 
      iex> Metaheuristique.get_all_data([[1, 2, 3, ...])
      %{
        number_of_objects: 1,
        number_of_bags: 2,
        objects_values: [3],
        bags_capacities: [...],
        lists_of_weights: [[...], [...]]
      }
 
  """
  def get_all_data() do
    [number_of_objects, number_of_bags | rest] = build_list()
    {objects_values, rest} = Enum.split(rest, number_of_objects)
    {bags_capacities, rest} = Enum.split(rest, number_of_bags)
    lists_of_weights = Enum.chunk_every(rest, number_of_objects)
 
    %{
      number_of_objects: number_of_objects,
      number_of_bags: number_of_bags,
      objects_values: objects_values,
      bags_capacities: bags_capacities,
      lists_of_weights: lists_of_weights
    }
  end
 
  @doc """
  With a given list of object_values and lists_of_weights for each bag build n list of tuples {values, weight} where n is the number of bags
  For example:
    - Item 1 in BAG 1 have a value of 89 and a weight of 98
    - Item 1 in Bag 2 have a value of 89 and a weight of 78
    Will build [[{89, 98}], [{89, 78}]]
 
  ## Examples
 
      iex> Metaheuristique.build_tuples_list([98, 78], [89])
      [[{89, 98}], [{89, 78}]]
 
  """
  def build_tuples_list(%{lists_of_weights: lists_of_weights, objects_values: objects_values}) do
    Enum.map(lists_of_weights, fn list_of_weights ->
      Enum.zip(objects_values, list_of_weights)
    end)
  end
 
  @doc """
  With a given list containing n list of tuples {values, weight} where n is the number of bags get the ratio value / weight for each item in each bag
  For example:
    - Item 1 in BAG 1 = {8, 10} gives a ratio of 0.8
    - Item 1 in Bag 2 = {100, 10} gives a ratio of 10
 
  ## Examples
 
      iex> Metaheuristique.get_ratio_by_items_in_bag([[{100, 87}, {23, 45}], [...]])
      [[1.14, 0.5], [...]]
 
  """
  def get_ratio_by_items_in_bag(tuples_lists) do
    Enum.map(tuples_lists, fn list_tuples ->
      Enum.map(list_tuples, fn tuple ->
        elem(tuple, 0) / elem(tuple, 1)
      end)
    end)
  end
 
  @doc """
  With a given list containing lists (one list per bag) of ratio values find the best ratio value/weight for each items.
  Then sort each ratio and build a new sorted index list (first index are the best ratio).
  For example:
    - Item 1 in BAG 1 ratio = 0.8
    - Item 1 in Bag 2 ratio = 10
    Gives a ratio of 0.8 + 10 = 10.8 that is better than a Ratio2 of 8.7
    So the list will be [Ratio1 Index, Ratio2 Index, ...]
 
  ## Examples
 
      iex> Metaheuristique.get_best_items_indexes([[1.14, 0.5], [...]])
      [1, 2, ...]
 
  """
  def get_best_items_indexes(ratio_lists) do
    ratio_lists
    |> List.zip()
    |> Enum.map(fn tuple -> Tuple.sum(tuple) end)
    |> Enum.with_index()
    |> Enum.sort(:desc)
    |> Enum.map(fn tuple ->
      elem(tuple, 1)
    end)
  end
 
  @doc """
  Fill all the bags based on the best ratio list. 
  The first items that we try to insert are the items with best ratios.
  If a bag can't accept the new item we try to insert the next one until there is no item left.
  Final result is a tuple {[indexes], [weights]} 
  This list contains all the indexes of the items we took & the final weights of each bags.
 
  ## Examples
 
      iex> Metaheuristique.fill_all_bags([89, 23, 92], data, tuples_lists)
      {[89, 92, 43, 87, ...], [11222, 13131, 11538, 10136, 11733]}
 
  """
  def fill_all_bags(index_list, %{bags_capacities: bags_capacities, number_of_bags: number_of_bags}, tuples_lists) do
      Enum.reduce(index_list, {[], []}, fn index, {indexes, weights} = acc ->
        Enum.map(0..number_of_bags-1, fn bag -> 
          weight = elem(Enum.at(Enum.at(tuples_lists, bag), index), 1) + Enum.at(weights, bag, 0)
          if weight <= Enum.at(bags_capacities, bag), do: weight, else: false
        end)
        |> fit_in_bags?(index, indexes, acc)
      end)
  end

  @doc """
  Based on the tuple of final bags weights and indexes we build a map with the final infos.
 
  ## Examples
 
      iex> Metaheuristique.calculate_value({[89, ...], [1982, ...]} data)
      %{
        bags_weight: [11222, 13131, 11538, 10136, 11733],
        items_indexes: [89, 92, 43, 87, ...], 
        total_value: 20158
      }
 
  """
  def calculate_value({indexes, weigths}, %{objects_values: values}) do
    total_value = Enum.map(indexes, fn index -> Enum.at(values, index) end) |> Enum.sum
    %{bags_weight: weigths, item_indexes: indexes, total_value: total_value}
  end

  defp fit_in_bags?(weights, index, indexes, acc), 
    do: if Enum.member?(weights, false), do: acc, else: {indexes ++ [index], weights}
 
  def main() do
    data = get_all_data()
 
    tuples_lists = build_tuples_list(data)

    tuples_lists
    |> get_ratio_by_items_in_bag()
    |> get_best_items_indexes()
    |> fill_all_bags(data, tuples_lists)
    |> calculate_value(data)
  end
end
 