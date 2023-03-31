using JuMP
using GLPK

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
function reader(filepath :: String)
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
path = "./instances/instance_20.dat"
graph = reader(path)