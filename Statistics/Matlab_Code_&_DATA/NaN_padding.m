function [matrix] = NaN_padding(dist)
matrix = cell(1,6);

for(k=1:6)

    sz = 0;
        for(i=1:4)
        [~,y] = size(dist{i,k});
            if(y>sz)
                sz = y;
            end
        end
    mat = zeros(4,sz);
    for(i=1:4)
        [~,y] = size(dist{i,k});
        for(j=1:sz)
            if(j<=y)
                mat(i,j) = dist{i,k}(1,j);
            else
                mat(i,j) = nan;
            end
        end
    end
    matrix{1,k} = mat;
end
end