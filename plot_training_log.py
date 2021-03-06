#!/usr/bin/env python
# NoaArbel edited plot_training_log.py
# There is an option to plot two graphs in the same image (such as training and test loss vs inters)
import inspect
import os
import random
import sys
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.legend as lgd
import matplotlib.markers as mks

def get_log_parsing_script():
    dirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return dirname + '/parse_log.sh'

def get_log_file_suffix():
    return '.log'

def get_chart_type_description_separator():
    return '  vs. '

def is_x_axis_field(field):
    x_axis_fields = ['Iters', 'Seconds']
    return field in x_axis_fields

def create_field_index():
    train_key = 'Train'
    test_key = 'Test'
    field_index = {train_key:{'Iters':0, 'Seconds':1, train_key + ' loss':2,
                              train_key + ' learning rate':3},
                   test_key:{'Iters':0, 'Seconds':1, test_key + ' accuracy':2,
                             test_key + ' loss':3}}
    fields = set()
    for data_file_type in field_index.keys():
        fields = fields.union(set(field_index[data_file_type].keys()))
    fields = list(fields)
    fields.sort()
    return field_index, fields

def get_supported_chart_types():
    field_index, fields = create_field_index()
    num_fields = len(fields)
    supported_chart_types = []
    # For one value plot
    for i in xrange(num_fields):
        if not is_x_axis_field(fields[i]):
            for j in xrange(num_fields):
                if i != j and is_x_axis_field(fields[j]):
                    str_temp = '%s%s%s' % (
                        fields[i], get_chart_type_description_separator(),
                        fields[j])
                    supported_chart_types.append(str_temp)
    # For two-values plot
    for i in xrange(num_fields):
        if not is_x_axis_field(fields[i]):
            for j in xrange(num_fields):
                for k in xrange(num_fields):
                    if not is_x_axis_field(fields[k]):
                        if i != j and k!=j and k!=i and is_x_axis_field(fields[j]):
                            str_temp = '%s%s%s%s%s' % (
                                fields[i],' and ',fields[k],get_chart_type_description_separator(),
                                fields[j])
                            supported_chart_types.append(str_temp)
    return supported_chart_types

def get_chart_type_description(chart_type):
    supported_chart_types = get_supported_chart_types()
    chart_type_description = supported_chart_types[chart_type]
    return chart_type_description

def get_data_file_type(chart_type):
    description = get_chart_type_description(chart_type)
    data_file_type = description.split()[0]
    description_temp = description.split(' and ')
    if len(description_temp) > 1: # more then one line to plot
        data_file_type2 = description_temp[1].split()[0]
    else:
        data_file_type2 = []
    return data_file_type, data_file_type2

def get_data_file(chart_type, path_to_log):
    data_file_description,data_file_description2 = get_data_file_type(chart_type)
    if data_file_description2:
        file1 = os.path.basename(path_to_log) + '.' + data_file_description.lower()
        file12 = os.path.basename(path_to_log) + '.' + data_file_description2.lower()
    else:
        file1 = os.path.basename(path_to_log) + '.' + data_file_description.lower()
        file12 = []
    return file1,file12

def get_field_descriptions(chart_type):
    description = get_chart_type_description(chart_type).split(
        get_chart_type_description_separator())
    description0 = description[0].split(' and ')
    if len(description0) == 1:
        y_axis_field_1 = description[0]
        y_axis_field_2 = []
        x_axis_field = description[1]
    else:
       if len(description0) == 2:
            y_axis_field_1 = description0[0]
            y_axis_field_2 = description0[1]
            x_axis_field = description[1]
    return x_axis_field, y_axis_field_1, y_axis_field_2

def get_field_indecies(x_axis_field, y_axis_field):    
    data_file_type, data_file_type2 = get_data_file_type(chart_type)
    file_type =  y_axis_field.split()[0] # Test or train
    fields = create_field_index()[0][file_type]
    return fields[x_axis_field], fields[y_axis_field]

def load_data(data_file, field_idx0, field_idx1):
    data = [[], []]
    with open(data_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line[0] != '#':
                fields = line.split()
                data[0].append(float(fields[field_idx0].strip()))
                data[1].append(float(fields[field_idx1].strip()))
    return data

def random_marker():
    markers = mks.MarkerStyle.markers
    num = len(markers.values())
    idx = random.randint(0, num - 1)
    return markers.values()[idx]

def get_data_label(path_to_log):
    description = get_chart_type_description(chart_type).split(' and ')
    if len(description) > 1: # more then one line to plot
        label = description[0]
        label2 = description[1].split(get_chart_type_description_separator())[0]
    else:
        label = description[0].split()[0]
        label2 = []
    return label,label2

def get_legend_loc(chart_type):
    x_axis, y_axis, y_axis2= get_field_descriptions(chart_type)
    loc = 'lower right'
    if y_axis.find('accuracy') != -1:
        pass
    if y_axis.find('loss') != -1 or y_axis.find('learning rate') != -1:
        loc = 'upper right'
    if y_axis2:
        if y_axis2.find('accuracy') != -1:
            pass
        if y_axis2.find('loss') != -1 or y_axis2.find('learning rate') != -1:
            loc = 'upper right'
    return loc

def plot_chart(chart_type, path_to_png, path_to_log_list):
    for path_to_log in path_to_log_list:
        os.system('%s %s' % (get_log_parsing_script(), path_to_log))
        data_file, data_file2 = get_data_file(chart_type, path_to_log)
        x_axis_field, y_axis_field,y_axis_field_2 = get_field_descriptions(chart_type)
        if not y_axis_field_2:
            x, y = get_field_indecies(x_axis_field, y_axis_field)
            data = load_data(data_file, x, y)
        else:
            x, y = get_field_indecies(x_axis_field, y_axis_field)
            x2, y2 = get_field_indecies(x_axis_field, y_axis_field_2)
            data = load_data(data_file, x, y)
            data2 = load_data(data_file2, x2, y2)
        ## TODO: more systematic color cycle for lines
        color = [random.random(), random.random(), random.random()]
        color2 = [random.random(), random.random(), random.random()]
        label,label2 = get_data_label(chart_type)
        linewidth = 0.75
        ## If there too many datapoints, do not use marker.
        if len(data[0])> 1000:
            use_marker = False
        else:
            use_marker = True
        if not use_marker:
            plt.plot(data[0], data[1], label = label, color = color,
                     linewidth = linewidth)
            if y_axis_field_2:
                plt.plot(data2[0], data2[1], label = label2, color = color2,
                     linewidth = linewidth)
        else:
            ok = False
            ## Some markers throw ValueError: Unrecognized marker style
            while not ok:
                try:
                    marker = random_marker()
                    plt.plot(data[0], data[1], label = label, color = color,
                             marker = marker, linewidth = linewidth)
                    if y_axis_field_2:
                        plt.plot(data2[0], data2[1], label = label2, color = color2,
                            marker = marker, linewidth = linewidth)
                    ok = True
                except:
                    pass
    legend_loc = get_legend_loc(chart_type)
    plt.legend(loc = legend_loc, ncol = 1) # ajust ncol to fit the space
    plt.title(get_chart_type_description(chart_type))
    plt.xlabel(x_axis_field)
    plt.ylabel(y_axis_field)  
    plt.savefig(path_to_png)     
    plt.show()

def print_help():
    print """This script mainly serves as the basis of your customizations.
Customization is a must.
You can copy, paste, edit them in whatever way you want.
Be warned that the fields in the training log may change in the future.
You had better check the data files and change the mapping from field name to
 field index in create_field_index before designing your own plots.
Usage:
    ./plot_training_log.py chart_type[0-%s] /where/to/save.png /path/to/first.log ...
Notes:
    1. Supporting multiple logs.
    2. Log file name must end with the lower-cased "%s".
Supported chart types:""" % (len(get_supported_chart_types()) - 1,
                             get_log_file_suffix())
    supported_chart_types = get_supported_chart_types()
    num = len(supported_chart_types)
    for i in xrange(num):
        print '    %d: %s' % (i, supported_chart_types[i])
    exit

def is_valid_chart_type(chart_type):
    return chart_type >= 0 and chart_type < len(get_supported_chart_types())
  
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_help()
    else:
        chart_type = int(sys.argv[1])
        if not is_valid_chart_type(chart_type):
            print_help()
        path_to_png = sys.argv[2]
        if not path_to_png.endswith('.png'):
            print 'Path must ends with png' % path_to_png
            exit            
        path_to_logs = sys.argv[3:]
        for path_to_log in path_to_logs:
            if not os.path.exists(path_to_log):
                print 'Path does not exist: %s' % path_to_log
                exit
            if not path_to_log.endswith(get_log_file_suffix()):
                print_help()
        ## plot_chart accpets multiple path_to_logs
        plot_chart(chart_type, path_to_png, path_to_logs)
