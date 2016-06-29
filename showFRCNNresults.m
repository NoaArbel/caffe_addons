% --------------------------------------------------------
% showFRCNNresults
% Licensed under The MIT License
% Noa Arbel, Technion
% --------------------------------------------------------

function h = showFRCNNresults(image,detections,classes_list,title_str)
% Show detection results on the image.
%
% inputes:
% image - the image
% detections - cell array of the detections (BB+scores of each class), in the fast-rcnn format
% classes_list - cell array with the classes names
% title_str - the figure title
%
% outputs:
% h - the figure handle

h = figure;
imshow(image);

colors_bb = hsv(length(detections));
for n=1:length(detections)
    boxes = detections{n};
    if ~isempty(boxes)
        x1 = boxes(:, 1);
        y1 = boxes(:, 2);
        x2 = boxes(:, 3);
        y2 = boxes(:, 4);
        c = colors_bb(n,:);
        s = '-';
        line([x1 x1 x2 x2 x1]', [y1 y2 y2 y1 y1]', ...
            'color', c, 'linewidth', 2, 'linestyle', s);
        for i = 1:size(boxes, 1)
            text(double(x1(i)), double(y1(i)) - 2, ...
                sprintf('%.3f', boxes(i, end)), ...
                'backgroundcolor', c, 'color', 'k','FontSize',6);
        end        
             text(-70,20*(n-1),...
                classes_list{n},...
                 'backgroundcolor', 'w', 'color', c);
    end
end
if (exist('title_str','var'))
    title(title_str);
end
end

