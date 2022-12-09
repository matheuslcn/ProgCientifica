# formato do json
# {
#     "conect": lista de conectividade,
#     "cc": lista de condições de contorno,
# }

using JSON

function readJson(filename::String)
    open(filename, "r") do file
        data = JSON.parse(file)
        if haskey(data,"connect")
            ne1 = size(data["connect"])[1]
            ne2 = size(data["connect"][1])[1]
            conect = zeros(Int64, ne1, ne2)
            for i = 1:ne1
                for j = 1:ne2
                    conect[i,j] = data["connect"][i][j]
                end
            end
        end
        if haskey(data,"cc")
            ne1 = size(data["cc"])[1]
            ne2 = size(data["cc"][1])[1]
            cc = zeros(Float64, ne1, ne2)
            for i = 1:ne1
                for j = 1:ne2
                    cc[i,j] = data["cc"][i][j]
                end
            end
        end
        return conect, cc
    end
end

function main(filename::String)
    # conect = [
    #      0    0    5    2
    #      1    0    6    3
    #      2    0    7    4
    #      3    0    8    0
    #      0    1    9    6
    #      5    2   10    7
    #      6    3   11    8
    #      7    4   12    0
    #      0    5   13   10
    #      9    6   14   11
    #     10    7   15   12
    #     11    8   16    0
    #      0    9    0   14
    #     13   10    0   15
    #     14   11    0   16
    #     15   12    0    0   ]


    # cc = [
    #     1   100
    #     1    75
    #     1    75
    #     1     0
    #     1   100
    #     0     0
    #     0     0
    #     1     0
    #     1   100
    #     0     0
    #     0     0
    #     1     0
    #     1   100
    #     1    25
    #     1    25
    #     1     0   ]

    conect, cc = readJson(filename)
    @show conect
    @show cc

    nn = size(conect)[1]
    A = zeros(Float64, nn, nn)
    b = zeros(Float64, nn, 1)
    for e = 1:nn
        if(cc[e,1] == 0)
            A[e,e] = -4
            A[e, conect[e,1]] = 1
            A[e, conect[e,2]] = 1
            A[e, conect[e,3]] = 1
            A[e, conect[e,4]] = 1
        else
            A[e,e] = 1
            b[e,1] = cc[e,2]
        end
    end

    x = A\b

    @show x
end


if length(ARGS) > 0
    main(ARGS[1])
end