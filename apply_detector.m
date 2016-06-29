% --------------------------------------------------------
% apply_detector
% Licensed under The MIT License
% Noa Arbel, Technion
% --------------------------------------------------------
function [dets_orig,dets,discarded_dets] = apply_detector(VOCopts, show_results_flag,...
    baseline_discard_th,proposals,I,do_nms,model)
% Apply fast-rcnn and discard low scoring results.
%
% inputes:
% VOCopts - PASCAL VOC data
% show_results_flag - if 1 (true) then we show the detection results.
% baseline_discard_th - discarding TH. can be eighter one value (same for all categories) or a vector size the number of categories (and then each class will have it's own TH.
% proposals - proposals for the detector, assuming selective search.
% I - the image
% do_nms - a flag that indicates if we want to apply NMS to the detection results (=1) or not (=0).
% model - the frcnn caffe model
%
% outputs:
% dets_orig - before thresholding the ouput
% dets - after thresholding


%% apply detector
% switch (x,y) in boxes (for Selective search input)
a = single(proposals);
a(:,5) = a(:,1); a(:,1) = a(:,2);a(:,2) = a(:,5);
a(:,5) = a(:,3); a(:,3) = a(:,4); a(:,4) = a(:,5);a(:,5) = [];
if (do_nms)
    dets = fast_rcnn_im_detect(model, I, a);
else
    dets = fast_rcnn_im_detect_without_nms(model, I, a);
    for  c = 1:length(dets)
        dets{c} = unique(dets{c},'rows');
    end
end
dets_orig = dets;

%% discard low detections each class with its own th
if (length(baseline_discard_th) == length(dets))    
    baseline_discard_th_vector = baseline_discard_th;
else
    if (length(baseline_discard_th)==1)
     baseline_discard_th_vector = repmat(baseline_discard_th,1,length(dets));
    end
end

empty_classes = ones(1,length(dets));
discarded_dets = cell(length(dets),1);
while (sum(empty_classes) == length(dets))
    for  c = 1:length(dets)
        discard_indx = dets{c}(:, end) <= baseline_discard_th_vector(c);
        discarded_dets{c} = dets{c}(discard_indx, :);
        dets{c}(discard_indx, :) = [];
        if (~isempty(dets{c}))
            empty_classes(c) = 0;
        end
    end
    if (sum(empty_classes) == length(dets))
        baseline_discard_th_vector(c) = baseline_discard_th_vector(c)./2;
        dets = dets_orig;
    end
end

%% Show results
if (show_results_flag)
    title_str = 'Original fast-rcnn results';
    showFRCNNresults(I,dets,VOCopts.classes,title_str);
end

end

