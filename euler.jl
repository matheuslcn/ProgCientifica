using JSON
using Plots

function func(t,y)
    fv = zeros(Float64, 2)
    fv[1] = 1.2 * y[1] - 0.6 * y[1] * y[2]
    fv[2] = -0.8 * y[2] + 0.3 * y[1] * y[2]
    return fv
end

function ya(t)
    return (t+1)*(t+1) - 0.5^t
end

function euler(_a,_w0, _h, _N)
    W = zeros(Float64, _N)
    W[1] = _w0
    for i = 1:_N-1
        W[i+1] = W[i] + _h * func(_a+(i-1)*_h,W[i])
    end
    return W
end

function euler2(_a,_w0::Vector{Float64}, _h, _N)
    W = zeros(Float64, 2, _N)
    W[1,1] = _w0[1]
    W[2,1] = _w0[2]
    for i = 1:_N-1
        W[:,i+1] = W[:,i] + _h * func(_a+(i-1)*_h,W[:,i])
    end
    return W
end

function rk(_a,_w0, _h, _N)
    W = zeros(Float64, _N)
    W[1] = _w0
    for i = 1:_N-1
        ti = _a+(i-1) * _h
        k1 = func(ti, W[i])
        k2 = func(ti+_h/2,W[i]+_h*k1/2)
        k3 = func(ti+_h/2,W[i]+_h*k2/2)
        k4 = func(ti+_h,W[i]+_h*k3)
        phi = k1/6+k2/3+k3/3+k4/6
        W[i+1] = W[i] + _h * phi
    end
    return W
end

function rk2(_a,_w0::Vector{Float64}, _h, _N)
    W = zeros(Float64,2, _N)
    W[1,1] = _w0[1]
    W[2,1] = _w0[2]
    for i = 1:_N-1
        ti = _a+(i-1) * _h
        k1 = func(ti, W[:,i])
        k2 = func(ti+_h/2,W[:,i]+_h*k1/2)
        k3 = func(ti+_h/2,W[:,i]+_h*k2/2)
        k4 = func(ti+_h,W[:,i]+_h*k3)
        phi = k1/6+k2/3+k3/3+k4/6
        W[:,i+1] = W[:,i] + _h * phi
    end
    return W
end

function main()
    println("main")
    a = 0.0
    b = 2.0
    h = 0.2
    w0 = zeros(Float64,2)
    w0[1] = 2
    w0[2] = 1
    N = Int64((b-a)/h)
    we = euler2(a, w0,h,N)
    wr = rk2(a, w0,h,N)
    t = zeros(Float64,N)
    t[1] = a
    wa = zeros(Float64, N)
    wa[1] = w0[1]
    for i = 1:N-1
        t[i+1] = a + i*h
        wa[i+1] = ya(t[i+1])
    end

    @show wa
    @show we
    @show wr
    # plot(t,wa)
    plot(t,we[1,:])
    plot!(t,we[2,:])
    plot!(t,wr[1,:])
    plot!(t,wr[2,:])
    # plot(t,wr)


end

if length(ARGS) == 0
    print("PROG")
    main()
else
    println(ARGS)
end
