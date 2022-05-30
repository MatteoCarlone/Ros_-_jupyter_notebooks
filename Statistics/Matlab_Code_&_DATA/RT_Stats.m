


%%
[dist_left, time_left]= Organizing_Dist(distleft1, distleft2 , distleft3, distleft4,distleft5);
%%
[dist_left_prof, time_left_prof] = Organizing_Dist(distleftProf1, distleftProf2 , distleftProf3, distleftProf4,distleftProf5);
%%
[dist_right,time_right] = Organizing_Dist(distright1, distright2 , distright3, distright4, distright5);
%%
[dist_right_prof,time_right_prof] = Organizing_Dist(distrightProf1, distrightProf2 , distrightProf3, distrightProf4,distrightProf5);
%% 
dl_mat = NaN_padding(dist_left);
dr_mat = NaN_padding(dist_right);
dl_P_mat = NaN_padding(dist_left_prof);
dr_P_mat = NaN_padding(dist_right_prof);
%%
time_dl_mat = NaN_padding(time_left);
time_dr_mat = NaN_padding(time_right);
time_dl_P_mat = NaN_padding(time_left_prof);
time_dr_P_mat = NaN_padding(time_right_prof);

%%
[lap, wd] = Lap_mean(laps1,laps2,laps3,laps4,laps5, ...
    laps6,laps7,laps8,laps9,laps10,laps11);

[lap_P, wd_P] = Lap_mean(lapsProf1,lapsProf2,lapsProf3,lapsProf4,lapsProf5, ...
    lapsProf6,lapsProf7,lapsProf8,lapsProf9,lapsProf10,lapsProf11);
%% Distance fill_between

std=cell(5,2);
m=cell(5,2);
down = cell(5,2);
up = cell(5,2);
t = cell(5,2);

for i=1:5
[m{i,1},t{i,1},std{i,1},down{i,1},up{i,1},m{i,2},t{i,2},std{i,2},down{i,2},up{i,2}]=Laps_Plot(dl_mat{1,i},time_dl_mat{1,i},...
    dl_P_mat{1,i},time_dl_P_mat{1,i});

end
%% Filtering
m_clean = cell(5,2);
t_clean = cell(5,2);
down_fill = down;

figure("Name","Lap1 , Lap2")

for j = 1:2
    for i = 1:2
        if i == 1
        RGB = [0,0.4470,0.7410];
        color = '#0072BD';
        else
        RGB = [0.8500,0.3250,0.0980];
        color = '#D95319';
        end
    
    [m_clean{j,i},t_clean{j,i}] = interpclean(m{j,i},t{j,i});
    
    [envhigh, envlow] = envelope(m_clean{j,i},10,'peak');
    envmean = (envhigh + envlow)/2;
    
    
    down_fill{1,i}(isnan(down{j,i})) = [];
        if(j==1)
            if(i==1)
                time_axe_x = linspace(0,lap(1),numel(envmean));
            else
                time_axe_x = linspace(0,lap_P(1),numel(envmean));
            end
        else
            if(i==1)
                time_axe_x = linspace(lap(1),lap(1)+lap(2),numel(envmean));
            else
                time_axe_x = linspace(lap_P(1),lap_P(1)+lap_P(2),numel(envmean));
            end
        end
        plot(time_axe_x,envmean,'Color',color)
        hold on
        [y1_h,y2_h,~]=fill_between(time_axe_x,down_fill{j,i},up{j,i},1, ...
        'EdgeColor','none','Facecolor',RGB,'FaceAlpha',0.15);
        
        y1_h.Color = 'none';
        y2_h.Color = 'none';
    end
end

ylim([0.3 2])

title('Average Left Obstacle distance & Standard Deviation, Lap1 and Lap2')
xlabel('Time [s]')
ylabel('Left Distance')


xline(lap(1),'--',{'Lap 1'},'LineWidth',2,'LabelOrientation', 'horizontal','Color','#0072BD','LabelHorizontalAlignment','left','LabelVerticalAlignment','bottom')
xline(lap(1)+lap(2),'--',{'Lap 2'},'LineWidth',2,'LabelOrientation', 'horizontal','Color','#0072BD','LabelHorizontalAlignment','left','LabelVerticalAlignment','bottom')

xline(lap_P(1),'--',{'Lap 1 Prof'},'LineWidth',2,'LabelOrientation', 'horizontal','Color','#D95319','LabelHorizontalAlignment','right','LabelVerticalAlignment','bottom')
xline(lap_P(1)+lap_P(2),'--',{'Lap 2 Prof'},'LineWidth',2,'LabelOrientation', 'horizontal','Color','#D95319','LabelHorizontalAlignment','right','LabelVerticalAlignment','bottom')

legend('std Lap1' , 'std Prof Lap1','std Lap2','std Prof Lap2','Average Dist Left','','','Average Dist Left Prof')
%% bar dist
mean_m = zeros(5,2);
std_m = zeros(5,2);
for i=1:5
    mean_m(i,1) = mean(m{i,1},'omitnan');
    mean_m(i,2) = mean(m{i,2},'omitnan');
    
    std_m(i,1) = mean(std{i,1},'omitnan');
    std_m(i,2) = mean(std{i,2},'omitnan');

end

figure()
x_tag_1 = ["lap1","lap2", "lap3", "lap4", "lap5"];
barwitherr(std_m,1:5,mean_m,'BarWidth',0.8,'LineWidth',1);

xticklabels(x_tag_1);
ylim([0,1.7])

xlabel('Laps')
ylabel('Right Distance')
title('Average Right Obstacle Distance & Standard deviation, for each lap')
legend('average dist right','average dist right prof','std','std prof')
grid on
%% Laps
figure()

x_tag_2 = ["lap1"," ","lap2"," ", "lap3"," ", "lap4"," ", "lap5"];

plot(1:5,lap(1:5),'s--', 'LineWidth',1.5,'MarkerSize',13,'MarkerEdgeColor','#000000','MarkerFaceColor','#0072BD')

hold on
plot(1:5,lap_P(1:5),'s--','LineWidth',1.5,'MarkerSize',13,'MarkerEdgeColor','#000000','MarkerFaceColor','#D95319')

xticklabels(x_tag_2);
xlim([0 6])
title("laps time")
legend("my lap","prof lap")
xlabel('Laps')
ylabel('Time [s]')
grid on

%% Wrong Direction
figure()

count = zeros(1,6);
count_P = zeros(1,6);

for i=1:5
    count(1,i) = sum(wd==i,'all');
    count_P(1,i) = sum(wd_P==i,'all');
end

total_count = sum(count);

total = 11 - total_count;

total_count_P = sum(count_P);

total_P = 11 - total_count_P;

count(1,6) = total;
count_P(1,6) = total_count_P;


explode = [0,0,1,0,0,0];
pr = pie3(count/11,explode);

pText = findobj(pr,'Type','text');
percentValues = get(pText,'String'); 
txt = {'wd Lap1: ';'wd Lap2 : ';'wd Lap3: ';'wd Lap4: ';'wd Lap5: ';'clean-lap: '}; 
combinedtxt = strcat('\fontsize{30}\bf',txt,percentValues); 

pText(1).String = combinedtxt(1);
pText(2).String = combinedtxt(2);
pText(3).String = combinedtxt(3);
pText(4).String = combinedtxt(4);
pText(5).String = combinedtxt(5);
pText(6).String = combinedtxt(6);

colormap bone

title("Wrong-Direction, Mine Robot",'FontSize',40)
%% WD Professor's robot
figure()
explode_P = [0,1,0,0,0,0];
pr_P = pie3(count_P/11,explode_P);

pText = findobj(pr_P,'Type','text');
percentValues = get(pText,'String'); 
txt = {'wd Lap1: ';'wd Lap2 : ';'wd Lap3: ';'wd Lap4: ';'wd Lap5: ';'clean-lap: '}; 
combinedtxt = strcat('\fontsize{30}\bf',txt,percentValues); 

pText(1).String = combinedtxt(1);
pText(2).String = combinedtxt(2);
pText(3).String = combinedtxt(3);
pText(4).String = combinedtxt(4);
pText(5).String = combinedtxt(5);
pText(6).String = combinedtxt(6);

colormap copper

title("Wrong-Direction, Professor Robot",'FontSize',40)


%%  Paired Ttest Distance

[h1, p1] = lillietest(mean_m(:,1)-mean_m(:,2),'MCTol',0.005)

[h,p ,c] = ttest(mean_m(:,1),mean_m(:,2))


%% Paired Ttest Lap

[h_lap,p_lap ,c_lap] = ttest(lap(:,1),lap_P(:,1))








