function [m,t] = interpclean(m,t)

    X = ~isnan(m);
    Y = cumsum(X-diff([1,X])/2);
    m = interp1(1:nnz(X),m(X),Y);
    rm = isnan(m);
    m(isnan(m))= [];
    t(rm) = [];

end