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
function createGraph(filepath :: String)
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

path = "./instances/instance_1000.dat"
graph = createGraph(path)
f = open(path, "r")
lines = readlines(f)
instanceLenght = parse(Int, lines[1])
close(f)

model = Model(GLPK.Optimizer);

# Definindo as variáveis do modelo
n_vertices = instanceLenght  # número de vértices do grafo
@variable(model, x[i=1:n_vertices, j=1:n_vertices], Bin)

@objective(model, Max, sum(x));

# Definindo as restrições do modelo
for i in 1:n_vertices
    @constraint(model, sum(x[j, i] for j in 1:n_vertices if (j, i) in graph.edges) + 
        sum(x[i, j] for j in 1:n_vertices if (i, j) in graph.edges) <= 2)
    @constraint(model,sum(x[j, i] for j in 1:n_vertices if !((j, i) in graph.edges)) + 
    sum(x[i, j] for j in 1:n_vertices if !((i, j) in graph.edges)) == 0)
end


# Create an empty graph
g = SimpleGraph(n_vertices)

# Add the edges to the graph
for e in graph.edges
    add_edge!(g, e[1], e[2])
end

cycles = cycle_basis(g)

# constraint pra impedir ciclos
for cycle in cycles
    cycle_edges = [(cycle[i], cycle[i+1]) for i=1:length(cycle)-1]
    cycle_edges = union(cycle_edges, [(cycle[end], cycle[1])])
    @constraint(model, sum(x[min(i,j),max(i,j)] for (i,j) in cycle_edges) <= length(cycle) - 1)
end
#println(model)
optimize!(model)
termination_status(model)

println("Solução:")
println(value(sum(x)))

for i in 1:n_vertices
    for j in 1:n_vertices
        if value(x[i, j]) == 1
            #println("Aresta de $i para $j está presente.")
        end
    end
end
