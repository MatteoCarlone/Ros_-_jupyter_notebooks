function [dist_lap, time_lap] = Organizing_Dist(dist1,dist2,dist3,dist4,dist5)
dist_lap = cell(4,6);
time_lap = cell(4,6);

for(lap=0:5)
    for(n=1:5)
        if n == 1
            x = dist1{1,3};
            k = 1;
            while(x ~= lap)
               k = k + 1;
               x = dist1{k,3}; 
            end
            i = 1;
            dist_c1=[];
            time_c1=[];
            while(x == lap)
                dist_c1(1,i) = dist1{k,1};
                time_c1(1,i) = dist1{k,2};
                k = k+1;
                i = i + 1;
                x = dist1{k,3};
            end
            dist_lap{1,lap+1} = dist_c1;
            time_lap{1,lap+1} = time_c1;
            
        end
        if n == 2
            x = dist2{1,3};
            k = 1;
            while(x ~= lap)
               k = k + 1;
               x = dist2{k,3}; 
            end
            i = 1;
            dist_c2=[];
            time_c2=[];
            while(x == lap)
                dist_c2(1,i) = dist2{k,1};
                time_c2(1,i) = dist2{k,2};
                k = k+1;
                i = i + 1;
                x = dist2{k,3};
            end
            dist_lap{2,lap+1} = dist_c2;
            time_lap{2,lap+1} = time_c2;
        end
        if n == 3
            x = dist3{1,3};
            k = 1;
            while(x ~= lap)
               k = k + 1;
               x = dist3{k,3}; 
            end
            i = 1;
            dist_c3=[];
            time_c3=[];
            while(x == lap)
                dist_c3(1,i) = dist3{k,1};
                time_c3(1,i) = dist3{k,2};
                k = k+1;
                i = i + 1;
                x = dist3{k,3};
            end
            dist_lap{3,lap+1} = dist_c3;
            time_lap{3,lap+1} = time_c3;

        end
        if n == 4
            x = dist4{1,3};
            k = 1;
            while(x ~= lap)
               k = k + 1;
               x = dist4{k,3}; 
            end
            i = 1;
            dist_c4=[];
            time_c4=[];
            while(x == lap)
                dist_c4(1,i) = dist4{k,1};
                time_c4(1,i) = dist4{k,2};
                k = k+1;
                i = i + 1;
                x = dist4{k,3};
            end
            dist_lap{4,lap+1} = dist_c4;
            time_lap{4,lap+1} = time_c4;
        end
        if n == 5
            x = dist5{1,3};
            k = 1;
            while(x ~= lap)
               k = k + 1;
               x = dist5{k,3}; 
            end
            i = 1;
            dist_c5=[];
            time_c5=[];
            while(x == lap)
                dist_c5(1,i) = dist5{k,1};
                time_c5(1,i) = dist5{k,2};
                k = k+1;
                i = i + 1;
                x = dist5{k,3};
            end
            dist_lap{1,lap+1} = dist_c5;
            time_lap{1,lap+1} = time_c5;
            
        end
        
    end

end
% Soglia

for(lap=1:6)
    for(n=1:4)
    [~, columns] = size(dist_lap{n,lap});
    for(j = 1:columns)
        if(dist_lap{n,lap}(1,j) > 2 || dist_lap{n,lap}(1,j) == 0)
            dist_lap{n,lap}(1,j) = nan;
        end
    end
    end
end

end