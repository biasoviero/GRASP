using Pkg
Pkg.add("JuMP")
Pkg.add("HiGHS")
Pkg.add("Random")

using JuMP
using HiGHS
using Random

function read_file(file_path)
    open(file_path, "r") do file
        n = parse(Int, readline(file))
        M = parse(Int, readline(file))
        T = parse(Int, readline(file))
        m = parse(Int, readline(file))
        
        attractions = []
        for _ in 1:m
            theme, dimension = split(readline(file)) .|> x -> parse(Int, string(x))
            push!(attractions, (theme, dimension))
        end
        
        return n, M, T, m, attractions
    end
end

function create_model(n, M, T, m, attractions)
    model = Model(HiGHS.Optimizer)

    @variable(model, x[1:n, 1:m], Bin)
    @variable(model, y[1:n, 1:T], Bin)

    # a soma das dimensões das atrações alocadas em um determinado espaço não podem ser maiores do que a metragem disponível
    for i in 1:n
        @constraint(model, sum(x[i, j] * attractions[j][2] for j in 1:m) <= M)
    end

    # cada atração pode ser alocada só uma vez
    for j in 1:m
        @constraint(model, sum(x[i, j] for i in 1:n) == 1)
    end

    # se uma atração j com o tema Tj está alocada no espaço i, então o tema Tj deve estar presente nesse espaço i
    for j in 1:m
        for i in 1:n
            theme = attractions[j][1]  # tema da atração j
            @constraint(model, x[i, j] <= y[i, theme])
        end
    end
    
    @objective(model, Min, sum(y[i, t] for i in 1:n, t in 1:T))
    
    return model, x, y
end

function main(args)

    if length(args) != 3
        println("Parâmetros incorretos! siga este padrão: julia script.jl <file_path> <seed> <timeout>")
        return
    end

    file_path = args[1]
    seed = parse(Int, args[2])
    timeout = parse(Int, args[3])

    Random.seed!(seed)

    n, M, T, m, attractions = read_file(file_path)

    model, x, y = create_model(n, M, T, m, attractions)

    set_time_limit_sec(model, timeout)
    
    set_attribute(model, "random_seed", seed)
    
    optimize!(model)

    status = JuMP.termination_status(model)
    
    if status == MOI.OPTIMAL || (status == MOI.TIME_LIMIT && JuMP.primal_status(model) == MOI.FEASIBLE_POINT)
        valor_objetivo = objective_value(model)
        solution_x = JuMP.value.(x)  
        
        println("Melhor solucão encontrada: $valor_objetivo")
        println("detalhes da solução:")
        for i in 1:n
            atracoes_atribuidas = [j for j in 1:m if solution_x[i, j] > 0.5]
            println("Espaço $i) atrações: $atracoes_atribuidas")
        end
    else
        println("Nenhuma solucão factível encontrada no tempo limite") 
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS)
end

# como executar: julia form_inteira.jl <file_path> <seed> <timeout>
# exemplo:
# julia form_inteira.jl 04.txt 10 5 