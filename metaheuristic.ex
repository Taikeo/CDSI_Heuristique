defmodule Metaheuristique do
  @moduledoc """
  Documentation for `Metaheuristique`.
  """
 
  @doc """
  Build a list from the input text file
 
  ## Examples
 
      iex> Metaheuristique.build_list("100M5_1.txt")
      [100, 5, 504]
 
  """
  def build_list() do
    if {:ok, text} = File.read("100M5_1.txt") do
      String.replace(text, "\n", "")
      |> String.replace(~r/ +/, " ")
      |> String.trim()
      |> String.split(" ")
      |> Enum.map(&String.to_integer/1)
    else
      {:error, "Erreur lors de la lecture du fichier"}
    end
  end
 
  @doc """
  With given lists of object_values and lists_of_weights for each bag build n list of tuples {values, weight} where n is the number of bags
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
 
  def first_solution(tuples_lists, data) do
    filled_bags = fill_all_bags(tuples_lists, data)
    maximum_number_of_items = get_max_number_of_items(filled_bags)
    optimal_bags = get_optimal_bags(maximum_number_of_items, filled_bags)
 
    build_data_map(optimal_bags)
  end
 
  def fill_all_bags(tuples_lists, %{bags_capacities: bags_capacities}) do
    tuples_lists
    |> Enum.with_index(fn elem, index -> {index, elem} end)
    |> Enum.map(fn {index, tuples_list} ->
        Enum.reduce_while(tuples_list, {0, []}, fn {value, weight}, acc ->
          if weight + elem(acc, 0) <= Enum.at(bags_capacities, index) do
            {:cont, {weight + elem(acc, 0), elem(acc, 1) ++ [{value, weight}]}}
          else
            {:halt, acc}
          end
        end)
      end)
  end
 
  def get_max_number_of_items(filled_bags) do
    Enum.map(filled_bags, fn {_weight, tuple_list} ->
      length(tuple_list)
    end)
    |> Enum.min()
  end
 
  def get_optimal_bags(max_number_of_items, filled_bags) do
    Enum.map(filled_bags, fn {_weight, tuple_list} ->
      Enum.take(tuple_list, max_number_of_items)
    end)
  end
 
  def build_data_map(full_bags) do
    Enum.map(full_bags, fn full_bag ->
      Enum.reduce(full_bag, %{value: 0, weight: 0}, fn {value, weight}, acc ->
        %{value: value + Map.get(acc, :value), weight: weight + Map.get(acc, :weight)}
      end)
      |> Map.put(:items, full_bag)
    end)
  end
 
  def main() do
    iteration_number = 10
    data = get_all_data()
    tuples_lists = build_tuples_list(data)
    first_solution = first_solution(tuples_lists, data)
    #|> IO.inspect(charlists: :as_lists)
 
    taboo_search(first_solution, tuples_lists, data, [], {0, iteration_number})
    1
  end
 
  def taboo_search(precedent_solution, tuples_lists, data, precedent_ban_list, iteration_nb, number_of_ban \\ 10)
 
  def taboo_search(precedent_solution, _, _, _, {current, it_number}, _) when current == it_number do
    precedent_solution
  end
 
  def taboo_search(precedent_solution, tuples_lists, data, precedent_ban_list, iteration_nb, number_of_ban) do
    new_ban_list = get_ban_list(precedent_solution, precedent_ban_list, number_of_ban)
 
    new_tuples_lists =
      tuples_lists
      |> Enum.with_index(fn element, index -> {index, element} end)
      |> Enum.map(fn {index, tuples_list} ->
        tuples_list -- Enum.at(new_ban_list, index)
      end)
 
    new_solution = first_solution(new_tuples_lists, data)
 
    IO.inspect(Map.get(Enum.at(precedent_solution, 0), :value), label: "VALUE 1")
    IO.inspect(Map.get(Enum.at(new_solution, 0), :value), label: "VALUE 2")
 
    if Map.get(Enum.at(precedent_solution, 0), :value) < Map.get(Enum.at(new_solution, 0), :value) do
      taboo_search(new_solution, tuples_lists, data, new_ban_list, {elem(iteration_nb, 0) + 1, elem(iteration_nb, 1)}, number_of_ban)
    else
      taboo_search(precedent_solution, tuples_lists, data, new_ban_list, {elem(iteration_nb, 0) + 1, elem(iteration_nb, 1)}, number_of_ban)
    end
  end
 
  def get_ban_list(precedent_solution, precedent_ban_list, number_of_ban) do
    bags_size = length(Map.get(Enum.at(precedent_solution, 0), :items))
    taboo_ban_index = Enum.take_random(0..bags_size - 1, number_of_ban)
 
    new_banned_items =
      precedent_solution
      |> Enum.map(fn %{items: items} ->
        items
        |> Stream.with_index()
        |> Stream.reject(fn {_item, index} -> index in taboo_ban_index end)
        |> Enum.map(&elem(&1, 0))
      end)
 
    if precedent_ban_list == [] do
      new_banned_items
    else
      precedent_ban_list
      |> Enum.zip(new_banned_items)
      |> Enum.map(fn zipped ->
        zipped
        |> Tuple.to_list()
        |> List.flatten()
      end)
    end
  end
end