using JuMP
using GLPK
using Graphs

function isPerfectSquare(n::Int)
    if (ceil(sqrt(n)) == floor(sqrt(n)))
        return true
    else
        return false
    end
end

struct Graph
    vertices::Vector{Int}
    edges::Vector{Tuple{Int,Int}}
end

function createGraph(filepath::String)
    f = open(filepath, "r")
    lines = readlines(f)
    instanceLenght = parse(Int, lines[1])
    data = split(lines[2])
    close(f)
    vertices = Vector{Int}()
    edges = Vector{Tuple{Int,Int}}()
    for i in 1:instanceLenght
        number1 = parse(Int, data[i])
        push!(vertices,number1)
        for j in i+1:instanceLenght
            number2 = parse(Int, data[j])
            if isPerfectSquare(number1+number2)
                push!(edges,(i,j))
            end
        end
    end
    return Graph(vertices,edges)
end
@time begin
path = "./instances/instance_1000.dat"
graph = createGraph(path)
f = open(path, "r")
lines = readlines(f)
instanceLenght = parse(Int, lines[1])
close(f)

n_vertices = instanceLenght  # número de vértices do grafo
n_edges = length(graph.edges) # número de arestas do grafo
model = Model(GLPK.Optimizer)

# Definindo as variáveis do modelo
@variable(model, x[1:n_edges], Bin)

@objective(model, Max, sum(x))
# Create an empty graph
g = SimpleGraph(n_vertices)

# Add the edges to the graph
for e in graph.edges
    add_edge!(g, e[1], e[2])
end

# Definindo as restrições do modelo
for i in 1:n_vertices
    edges_in = [ idx for (idx, (u, v)) in enumerate(graph.edges) if  v == i]
    edges_out = [ idx for (idx, (u, v)) in enumerate(graph.edges) if u == i]
    @constraint(model, sum(x[idx] for idx in edges_in) + sum(x[idx] for idx in edges_out)<= 2)
end


cycles = cycle_basis(g)
# constraint pra impedir ciclos
for cycle in cycles
    cycle_edges = [(cycle[i], cycle[i+1]) for i=1:length(cycle)-1]
    cycle_edges = union(cycle_edges, [(cycle[end], cycle[1])])
    edge_indices = [idx for (idx, e) in enumerate(graph.edges) if e in cycle_edges || reverse(e) in cycle_edges]
    @constraint(model, sum(x[e_idx] for e_idx in edge_indices) <= length(cycle) - 1)
end

# Resolve o modelo
optimize!(model)
termination_status(model)

println("Solução:")
println(value(sum(x)))
end