function [laps, wrong_direction] = Lap_mean(lap1,lap2,lap3,lap4,lap5, ...
    lap6,lap7,lap8,lap9,lap10,lap11)

    [lap1,wd1]= Organizing_Lap(lap1);
    [lap2,wd2]= Organizing_Lap(lap2);
    [lap3,wd3]= Organizing_Lap(lap3);
    [lap4,wd4]= Organizing_Lap(lap4);
    [lap5,wd5]= Organizing_Lap(lap5);
    [lap6,wd6]= Organizing_Lap(lap6);
    [lap7,wd7]= Organizing_Lap(lap7);
    [lap8,wd8]= Organizing_Lap(lap8);
    [lap9,wd9]= Organizing_Lap(lap9);
    [lap10,wd10]= Organizing_Lap(lap10);
    [lap11,wd11]= Organizing_Lap(lap11);

    laps = [lap1,lap2,lap3,lap4,lap5,lap6,lap7,lap8,lap9,lap10,lap11];

    laps = mean(laps,2,'omitnan');

    wrong_direction = [wd1;wd2;wd3;wd4;wd5;wd6;wd7;wd8;wd9;wd10;wd11]

end