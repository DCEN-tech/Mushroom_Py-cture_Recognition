# -*- coding: utf-8 -*-

from collections import namedtuple
from IPython.display import display, Markdown



def printAISettings(settings):
   if not settings:
      return

   display(Markdown('**AI Settings Summary**: '))

   markdownTxt = f'<table style="border: 1px solid black; border-collapse: collapse;">'

   # model parameters
   params = settings.get('model')
   if params:
      markdownTxt += f'''
         <tr><th colspan=2 style='border: 1px solid black; border-collapse: collapse;'>MODEL</th></tr>
         <tr><th>model_name</th><td>{params.get('model_name')}</td></tr>
         <tr><th>model_input_shape</th><td>{params.get('model_input_shape')}</td></tr>
         <tr><th>transfer_learning</th><td>{params.get('transfer_learning')}</td></tr>
         <tr><th>model_fine_tuning</th><td>{params.get('model_fine_tuning')}</td></tr>'''

   # model_optimization
   params = settings.get('model_optimization')
   if params:
      markdownTxt += f'''
         <tr><th colspan=2 style='border: 1px solid black; border-collapse: collapse;'>MODEL OPTIMIZATION</th></tr>
         <tr><th>optimizer_name</th><td>{params.get('optimizer_name')}</td></tr>
         <tr><th>loss_name</td><td>{params.get('loss_name')}</td></tr>
         <tr><th>dynamic_learning_rate</th><td>{params.get('dynamic_learning_rate')}</td></tr>'''

   # model_learning
   params = settings.get('model_learning')
   if params:
      markdownTxt += f'''
         <tr><th colspan=2 style='border: 1px solid black; border-collapse: collapse;'>MODEL LEARNING</th></tr>
         <tr><th>epochs</th><td>{params.get('epochs')}</td></tr>
         <tr><th>batch_size</th><td>{params.get('batch_size')}</td></tr>'''

   # dataset
   params = settings.get('dataset')
   if params:
      markdownTxt += f'''
         <tr><th colspan=2 style='border: 1px solid black; border-collapse: collapse;'>DATASET</th></tr>
         <tr><th>target_image_shape</th><td>{params.get('target_image_shape')}</td></tr>
         <tr><th>target_color_mode</th><td>{params.get('target_color_mode')}</td></tr>
         <tr><th>image_augmentation</th><td>{params.get('data_augmentation')}</td></tr>
         <tr><th>nb_genus</th><td>{params.get('nb_genus')}</td></tr>
         <tr><th>max_images_per_genus</th><td>{params.get('max_images_per_genus')}</td></tr>'''

   # random
   params = settings.get('random')
   if params:
      markdownTxt += f'''
         <tr><th colspan=2 style='border: 1px solid black; border-collapse: collapse;'>RANDOM</th></tr>
         <tr><th>seed</th><td>{params.get('seed')}</td></tr>
         <tr><th>seed_split_1</th><td>{params.get('seed_split_1')}</td></tr>
         <tr><th>seed_split_2</th><td>{params.get('seed_split_2')}</td></tr>'''

   markdownTxt += '</table>'

   display(Markdown(markdownTxt))



def printPathSettings(setting):
   display(Markdown('**Path Settings Summary**: '))

   display(Markdown(f'''
<table style='border: 1px solid black; border-collapse: collapse;'>
   <tr><th>model_output_run_dir</th><td>{setting.get('model_output_run_dir')}</td></tr>
   <tr><th>image_root_dir</th><td>{setting.get('image_root_dir')}</td></tr>
</table>
'''
   ))
