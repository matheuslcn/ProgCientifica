using Plots
using JSON
using Printf
# using benchmarkTools


function readJSON(_file::String)
    # println(".read")
    open(_file,"r") do f
        data = JSON.parse(f)
        if haskey(data,"coords")
            ne = size(data["coords"])[1]
            x0 = Array{Float64}(undef,ne,1)
            y0 = Array{Float64}(undef,ne,1)
            for i=1:ne
                x0[i] = convert(Float64,data["coords"][i][1])
                y0[i] = convert(Float64,data["coords"][i][2])
            end
        end
        if haskey(data, "connect")
            tam = size(data["connect"])[1]
            tamL = size(data["connect"][1])[1]
            conect = zeros(Int32, tam, tamL)
            for i = 1:tam
                for j = 1:tamL
                    conect[i,j] = data["connect"][i][j]
                end
            end
            # @show conect
        end
        if haskey(data, "F")
            tamF = size(data["F"])[1]
            F = zeros(Float64, tamF, 2)
            for i = 1:tamF
                F[i,1] = data["F"][i][1]
                F[i,2] = data["F"][i][2]
            end
            # @show F
        end
        if haskey(data, "restrs")
            tamRes = size(data["restrs"])[1]
            restrs = zeros(Int8,tamRes,2)
            for i = 1:tamRes
                restrs[i,1] = data["restrs"][i][1]
                restrs[i,2] = data["restrs"][i][2]
            end
            # @show restrs
        end
        return ne,x0,y0, conect, F, restrs
    end
end

function outputRes(_res)
    dict = Dict()
    push!(dict,"resultado"=>_res)
    open("output.json","w") do f
        JSON.print(f,dict)
    end
end

function printVetor(vetor, min, max, menorQue)
    if(menorQue)
        if(min < max)
            println(stderr, vetor)
            println(stderr, " ")
            println(stderr, " ")
        end
    else
        if(min == max)
            println(stderr, vetor)
            println(stderr, " ")
            println(stderr, " ")
        end
    end
end

function criaTabela(linha, pos, nome, vetor, size)
    # @printf("%d, %d, %s, ", linha, pos, nome);
    # for i = 1:size
    #         @printf("%.50f", vetor[i]);
    #         if (i <= size - 1)
    #             @printf(", ");
    #         end
    # end
    # @printf("\n");
end



function main(_file::String)
    # println(".DEM")
    # read input file
    N = 600
    h = 0.00004
    ne, x0, y0, conect, F, restrs = readJSON(_file)
    ndofs = 2*ne
    raio = 1.0
    mass = 7850.0
    kspr = 210000000000.0
    # conect = [
    #     2    2    4    0    0
    #     3    1    3    5    0
    #     2    2    6    0    0
    #     3    5    1    7    0
    #     4    4    6    2    8
    #     3    5    3    9    0
    #     3    8    4   10    0
    #     4    7    9    5   11
    #     3    8    6   12    0
    #     3   11    7   13    0
    #     4   10   12    8   14
    #     3   11    9   15    0
    #     3   14   10   16    0
    #     4   13   15   11   17
    #     3   14   12   18    0
    #     2   17   13    0    0
    #     3   16   18   14    0
    #     2   17   15    0    0    ]
    # F = [
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  0.00000     0.00000
    #  -1000.0     0.00000
    #  -1000.0     0.00000
    #  -1000.0     0.00000]
    # restrs = [
    #     1   1
    #     1   1
    #     1   1
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0
    #     0   0]
    F = reshape(transpose(F),(ndofs,1))
    restrs = reshape(transpose(restrs),(ndofs,1))

    # @show ne
    #@show x0
    #@show y0
    #@show conect
    #@show F
    #@show restrs

    u = zeros(Float64,ndofs,1)
    v = zeros(Float64,ndofs,1)
    a = zeros(Float64,ndofs,1)
    res = zeros(Float64,N)

    fi = zeros(Float64,ndofs,1)
    # @show fi
    # criaTabela(-2, 0, "X0", x0, ne)
    # criaTabela(-2, 1, "Y0", y0, ne)
    # criaTabela(-2, 2, "res", res, N)

    # criaTabela(-1, 0, "a", a, ndofs)
    # criaTabela(-1, 1, "F", F, ndofs)
    # criaTabela(-1, 2, "fi", fi, ndofs)
    tempo = @time begin
        a .= (F .- fi)./mass
        # criaTabela(-1, 3, "a", a, ndofs)
            # println(stderr, a)
            # println(stderr, " ")
            # println(stderr, " ")

        for i = 1:N
            # criaTabela(i-1, 0, "v", v, ndofs)
            v .+= a .* (0.5*h)
            # criaTabela(i-1, 1, "v", v, ndofs)
            # criaTabela(i-1, 2, "u", u, ndofs)
            u .+= v .* h
            # criaTabela(i-1, 3, "u", u, ndofs)

            # contato
            fi .= 0.0
            # criaTabela(i-1, 4, "fi", fi, ndofs)
            for j = 1:ne
                if (restrs[2*j-1] == 1)
                    u[2*j-1] = 0.0
                end
                if (restrs[2*j] == 1)
                    u[2*j] = 0.0
                end
                xj = x0[j] + u[2*j-1]
                yj = y0[j] + u[2*j]
                for index = 1:conect[j,1]
                    k = conect[j,index+1]
                    # (i==1) && @printf("%d, %d, 00, %.50f, %.50f, %.50f, %.50f\n", j-1, k, x0[k], y0[k], u[2 * k-1], u[2 * k]);

                    xk = x0[k] + u[2*k-1]
                    yk = y0[k] + u[2*k]
                    dX = xj-xk
                    # (i==1) && @printf("%d, %d, 01, dX: %.50f = xj: %.50f - xk: %.50f;\n", j-1, k, dX, xj, xk);
                    dY = yj-yk
                    # (i==1) && @printf("%d, %d, 02, dY: %.50f = yj: %.50f - yk: %.50f;\n", j-1, k, dY, yj, yk);
                    di = sqrt(dX*dX+dY*dY)
                    # (i==1) && @printf("%d, %d, 03, di: %.50f;\n", j-1, k, di);
                    d2 = (di - 2*raio)
                    # (i==1) && @printf("%d, %d, 04, d2: %.50f = di:%.50f - 2 * %.50f;\n", j-1, k, d2, di, raio);
                    dx = d2*dX/di
                    # (i==1) && @printf("%d, %d, 05, dx: %.50f;\n", j-1, k, dx);
                    dy = d2*dY/di
                    # (i==1) && @printf("%d, %d, 06, dy: %.50f;\n", j-1, k, dy);
                    # (i==1) && @printf("%d, %d, 07, saida_fi[%d]: %.50f;\n", j-1, k, 2*j-2, fi[2*j-1]);
                    # (i==1) && @printf("%d, %d, 08, saida_fi[%d]: %.50f;\n", j-1, k, 2*j-1, fi[2*j]);
                    fi[2*j-1] += kspr*dx
                    # (i==1) && @printf("%d, %d, 09, saida_fi[%d]: %.50f;\n", j-1, k, 2*j-2, fi[2*j-1]);
                    fi[2*j] += kspr*dy
                    # (i==1) && @printf("%d, %d, 10, saida_fi[%d]: %.50f;\n", j-1, k, 2*j-1, fi[2*j]);
                end
            end
            # criaTabela(i-1, 5, "fi", fi, ndofs)
            # criaTabela(i-1, 6, "u", u, ndofs)
            # criaTabela(i-1, 7, "X0", x0, ne)
            # criaTabela(i-1, 8, "Y0", y0, ne)

            a .= (F .- fi)./mass
            # criaTabela(i-1, 9, "a", a, ndofs)

            v .+= a .* (0.5*h)
            # criaTabela(i-1, 10, "v", v, ndofs)
            # plot
            res[i] = u[33]
            # criaTabela(i-1, 11, "res", res, N)

        end
    end
    @show tempo
    outputRes(res)
    #@show res
    x = 1:N
    # plot(x,res)
end

if length(ARGS) == 1
    main(ARGS[1])
end
