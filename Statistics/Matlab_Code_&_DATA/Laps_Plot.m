function [m_d_mat,m_t_mat,std_d_mat,down,up,m_d_P_mat,m_t_P_mat,std_d_P_mat,down_P,up_P] = Laps_Plot(d_mat,t_mat,d_P_mat,t_P_mat)
    

    m_d_mat = mean(d_mat,'omitnan');
    std_d_mat = std(d_mat, 'omitnan');

    m_t_mat = mean(t_mat,'omitnan');
    %m_t_mat = linspace(min(m_t_mat),max(m_t_mat),numel(m_t_mat));

    m_d_P_mat = mean(d_P_mat,'omitnan');
    std_d_P_mat = std(d_P_mat, 'omitnan');
    m_t_P_mat = mean(t_P_mat,'omitnan');
    
    m_t_P_mat = sort(m_t_P_mat);
    %m_t_P_mat = linspace(min(m_t_P_mat),max(m_t_P_mat),numel(m_t_P_mat));

    %plot(sort(m_t_mat),m_d_mat,color);

    %hold on 
    
    down = m_d_mat - std_d_mat;
    X_d = ~isnan(down);
    Y_d = cumsum(X_d-diff([1,X_d])/2);
    down = interp1(1:nnz(X_d),down(X_d),Y_d);
    %rm_d = isnan(down);
    %down(isnan(down))= [];
    %m_t_mat(rm_d) = [];
    
    up = m_d_mat + std_d_mat;
    X_u = ~isnan(up);
    Y_u = cumsum(X_u-diff([1,X_u])/2);
    up = interp1(1:nnz(X_u),up(X_u),Y_u);
    up(isnan(up))= [];
    
    %[y1_h,y2_h,~]=fill_between(sort(m_t_mat),down,up,1, ...
    %'EdgeColor','none','Facecolor',RGB,'FaceAlpha',0.15);

     %y1_h.Color = 'none';
    % y2_h.Color = 'none';
    
    %hold on 
    %plot(m_t_P_mat,m_d_P_mat,color_P);
    %xlim( [m_t_P_mat(1,25),m_t_P_mat(1,numel(m_t_P_mat))] );

   % hold on 
    down_P = m_d_P_mat - std_d_P_mat;

    X_d_P = ~isnan(down_P);
    Y_d_P = cumsum(X_d_P-diff([1,X_d_P])/2);
    down_P = interp1(1:nnz(X_d_P),down_P(X_d_P),Y_d_P);
    %rm_d_P = isnan(down_P);
    %down_P(isnan(down_P))= [];
    %m_t_P_mat(rm_d_P) = [];

    
    up_P = m_d_P_mat + std_d_P_mat;
    
    X_u_P = ~isnan(up_P);
    Y_u_P = cumsum(X_u_P-diff([1,X_u_P])/2);
    up_P = interp1(1:nnz(X_u_P),up_P(X_u_P),Y_u_P);
    up_P(isnan(up_P))= [];
    
    %[y1_h,y2_h,~]=fill_between(m_t_P_mat,down_P,up_P,1, ...
    %'EdgeColor','none','Facecolor',RGB_P,'FaceAlpha',0.15);

     %y1_h.Color = 'none';
     %y2_h.Color = 'none';
    

end