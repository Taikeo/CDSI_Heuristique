defmodule Metaheuristique do
  @moduledoc """
  Documentation for `Metaheuristique`.
  """
 
  @doc """
  Build a list from the input text file
 
  ## Example
 
      iex> Metaheuristique.build_list("100M5_1.txt")
      [100, 5, 504]
 
  """
  def build_list(instance) do
    if {:ok, text} = File.read("Instances/#{instance}.txt") do
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
 
  ## Example
 
      iex> Metaheuristique.get_all_data([[1, 2, 3, ...])
      %{
        number_of_objects: 1,
        number_of_bags: 2,
        objects_values: [3],
        bags_capacities: [...],
        lists_of_weights: [[...], [...]]
      }
 
  """
  def get_all_data(instance) do
    [number_of_objects, number_of_bags | rest] = build_list(instance)
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
 
  ## Example
 
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
 
  ## Example
 
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
 
  ## Example
 
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
 
  ## Example
 
      iex> Metaheuristique.fill_all_bags([89, 23, 92], data, tuples_lists)
      {[89, 92, 43, 87, ...], [11222, 13131, 11538, 10136, 11733]}
 
  """
  def fill_all_bags(index_list, %{bags_capacities: bags_capacities, number_of_bags: number_of_bags}, tuples_lists, ban_list \\ []) do
      Enum.reduce(index_list, {[], []}, fn index, {indexes, weights} = acc ->
        Enum.map(0..number_of_bags-1, fn bag -> 
          weight = elem(Enum.at(Enum.at(tuples_lists, bag), index), 1) + Enum.at(weights, bag, 0)
          if weight <= Enum.at(bags_capacities, bag), do: weight, else: false
        end)
        |> fit_in_bags?(index, indexes, acc, ban_list)
      end)
  end

  @doc """
  Based on the tuple of final bags weights and indexes we build a map with the final infos.
 
  ## Example
 
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

  @doc """
  Based on the precedent solution, banned items, and several other parameters.
  Build the ban list and then build a new solution with the items that are not banned.
  All solutions are kept in memory. 
  When the desired iteration number is reached find the best solution over the list of solutions and return it.
 
  ## Examples
 
      iex> Metaheuristique.taboo_search()
      %{
        bags_weight: [11222, 13131, 11538, 10136, 11733],
        items_indexes: [89, 92, 43, 87, ...], 
        total_value: 20158
      }
 
  """
  def taboo_search(precedent_solutions, _, _, _, {current, it_number}, _, _, _) when current == it_number do
    best_solution =
			Enum.map(precedent_solutions, fn solution -> 
				solution.total_value
			end)
			|> Enum.with_index()
			|> Enum.sort(:desc)
			|> Enum.at(0)

		Enum.at(precedent_solutions, elem(best_solution, 1))
  end
 
  def taboo_search(precedent_solutions, tuples_lists, data, precedent_ban_list, {current_iteration, iteration_nb}, number_of_ban, max_ban_nb, sorted_index_by_ratio) do
    new_ban_list = get_ban_list(Enum.at(precedent_solutions, 0), precedent_ban_list, number_of_ban, max_ban_nb)

		new_solution =
			sorted_index_by_ratio
			|> fill_all_bags(data, tuples_lists, new_ban_list)
			|> calculate_value(data)

		taboo_search([new_solution] ++ precedent_solutions, tuples_lists, data, new_ban_list, {current_iteration + 1, iteration_nb}, number_of_ban, max_ban_nb, sorted_index_by_ratio)
  end

  def write_in_text_file(%{item_indexes: item_indexes} = result, nb_of_items, instance) do
    items_to_take = List.duplicate(0, nb_of_items)
    index_list = Enum.reduce(item_indexes, items_to_take, &List.replace_at(&2, &1, 1)) |> Enum.join(" ")
    
    File.write("sol_#{instance}.txt", "#{result.total_value} #{index_list}")
    result
  end
 
  defp get_ban_list(%{item_indexes: precedent_indexes}, banned_indexes, nb_of_ban, max_ban_nb) do
    new_ban_indexes = Enum.take_random(precedent_indexes, nb_of_ban)

		Enum.take(new_ban_indexes ++ banned_indexes, max_ban_nb)
  end

  defp fit_in_bags?(weights, index, indexes, acc, ban_list), 
    do: if Enum.member?(weights, false) or Enum.member?(ban_list, index), do: acc, else: {indexes ++ [index], weights}
 
  def main(iteration_nb \\ 100, number_of_ban \\ 10, max_ban_nb \\ 20, instance \\ "100M5_1") do
    data = get_all_data(instance)
 
    tuples_lists = build_tuples_list(data)

    sorted_index_by_ratio =
			tuples_lists
			|> get_ratio_by_items_in_bag()
			|> get_best_items_indexes()

		first_solution =
			sorted_index_by_ratio
			|> fill_all_bags(data, tuples_lists)
			|> calculate_value(data)

    [first_solution]
		|> taboo_search(tuples_lists, data, [], {0, iteration_nb}, number_of_ban, max_ban_nb, sorted_index_by_ratio)
    |> write_in_text_file(data.number_of_objects, instance)
  end
end