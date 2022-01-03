import deepdream
import os
import utils.utils as utils
from utils.constants import *
import utils.video_utils as video_utils
import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title('Deep Dream')
root.geometry('800x600+50+50')
root.resizable(False,False)

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=3)


input  = tk.StringVar() #changes
input   ="cloud.jpg"
img_width  = tk.StringVar()
model_name  = tk.StringVar()
pretrained_weights  = tk.StringVar()
layers_to_use  = tk.StringVar()
pyramid_size  = tk.StringVar()
pyramid_ratio  = tk.StringVar()
num_gradient_ascent_iterations  = tk.StringVar()
lr  = tk.StringVar()
spatial_shift_size  = tk.StringVar()
smoothing_coefficient = tk.StringVar()
#use_noise  = tk.StringVar()
#create_ouroboros  = tk.StringVar()
#should_display  = tk.StringVar()


input_label = ttk.Label(root, text="input")
input_label.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=input)
input_textbox.grid(column=1, row=0, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=0, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="img_width")
input_label.grid(column=0, row=1, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=img_width)
input_textbox.grid(column=1, row=1, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=1, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="model_name")
input_label.grid(column=0, row=2, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=model_name)
input_textbox.grid(column=1, row=2, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=2, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="pretrained_weights")
input_label.grid(column=0, row=3, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=pretrained_weights)
input_textbox.grid(column=1, row=3, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=3, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="layers_to_use")
input_label.grid(column=0, row=4, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=layers_to_use)
input_textbox.grid(column=1, row=4, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=4, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="pyramid_size")
input_label.grid(column=0, row=5, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=pyramid_size)
input_textbox.grid(column=1, row=5, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=5, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="pyramid_ratio")
input_label.grid(column=0, row=6, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=pyramid_ratio)
input_textbox.grid(column=1, row=6, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=6, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="num_gradient_ascent_iteration")
input_label.grid(column=0, row=7, sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=num_gradient_ascent_iterations)
input_textbox.grid(column=1, row=7, sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=7, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="lr")
input_label.grid(column=0, row=8,sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=lr)
input_textbox.grid(column=1, row=8,sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=8, sticky=tk.W, padx=0, pady=5)

input_label = ttk.Label(root, text="spatial_shift_size")
input_label.grid(column=0, row=9,sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=spatial_shift_size)
input_textbox.grid(column=1, row=9,sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=9, sticky=tk.W, padx=0, pady=5)


input_label = ttk.Label(root, text="smoothing_coefficient")
input_label.grid(column=0, row=10,sticky=tk.E, padx=5, pady=5)
input_textbox = ttk.Entry(root, textvariable=smoothing_coefficient)
input_textbox.grid(column=1, row=10,sticky=tk.NS, padx=5, pady=5)
input_comment =ttk.Label(root, text="default: ")
input_comment.grid(column=2, row=10, sticky=tk.W, padx=0, pady=5)


#class SupportedModels(enum.Enum):
#    VGG16 = 0
#    VGG16_EXPERIMENTAL = 1
#    GOOGLENET = 2
#    RESNET50 = 3
#    ALEXNET = 4
#
#
#class SupportedPretrainedWeights(enum.Enum):
#    IMAGENET = 0
#    PLACES_365 = 1


config = dict()



def on_submit():
    config['input'] = input
    config['img_width'] = img_width
    config['model_name'] = model_name
    config['pretrained_weights'] = pretrained_weights
    config['layers_to_use'] = layers_to_use
    config['use_noise'] = False
    config['smoothing_coefficient'] = 0.5
    config['should_display'] = False
    config['create_ouroboros'] = False
    config['dump_dir'] = OUT_VIDEOS_PATH if config['create_ouroboros'] else OUT_IMAGES_PATH
    config['dump_dir'] = os.path.join(config['dump_dir'], f'{config["model_name"]}_{config["pretrained_weights"]}')
    config['input_name'] = os.path.basename(config['input'])
    
    img = deepdream.deep_dream_static_image(config,  img=None)
    dump_path = utils.save_and_maybe_display_image(config, img)
    print(f'Saved DeepDream static image to: {os.path.relpath(dump_path)}\n')





button = ttk.Button(root, text='Dawaj', command=on_submit)
button.grid(column=1)




root.mainloop()