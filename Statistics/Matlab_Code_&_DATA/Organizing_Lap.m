function [lap_o, wrong_direction] = Organizing_Lap(laps_t)
    lap_o = zeros(6,1);
    wrong_direction = [];
   
    laps(:,:) = laps_t{:,:};
    
    for i=1:6 
       
        if(i>=2)
            if(~isnan(laps(i,1)))
                lap_o(i,1)  = laps(i,2)-laps(i-1,2);
            else
                lap_o(i,1)  = NaN;
                wrong_direction(i) = laps(i,3);
            end

        else

            lap_o(i,1) = laps(i,2);

        end

        
    end

end