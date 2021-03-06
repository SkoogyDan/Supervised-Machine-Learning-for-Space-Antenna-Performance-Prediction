from pathlib import Path
from pandas import DataFrame
from torch.utils.data import random_split, Dataset
from torch.utils.data.dataloader import DataLoader
from matplotlib import pyplot as plt
from ssapp.data.AntennaDatasetLoaders import train_test_data_split
import numpy as np






def save_eps_figure(filename, subfolder = None, format = 'eps'):
    
    main_dir = Path().cwd().parents[1]
    fig_dir = main_dir / 'reports' / 'figures'
    if subfolder is not None:
        save_dir = fig_dir / subfolder / (filename+'.eps')
    else:
        save_dir = fig_dir / (filename+'.eps')

    plt.savefig(save_dir, format=format)

class FigureSaver():

    def __init__(self,subfolder = '', default_format = 'eps',bbox_inches='tight',dpi = 300,exstra_back_step = 0):
        self.bbox_inches = bbox_inches
        main_dir = Path().cwd().parents[1+exstra_back_step]
        fig_dir = main_dir / 'reports' / 'figures'
        self.fig_dir = fig_dir / subfolder
        self.format = default_format
        self.dpi = dpi

    def save(self,filename,save_format = 'default', fig = None):
    
        if save_format == 'default':
            save_format = self.format

        if fig is None:
            plt.savefig(self.fig_dir / (filename+'.'+save_format),format = save_format,dpi = self.dpi, bbox_inches=self.bbox_inches)

    def set_save_dir(self,path):
        self.fig_dir = Path

    def get_save_path(self):
        
        return self.fig_dir

    def __call__(self,filename,save_format = 'default', fig = None):
        self.save(filename,save_format, fig)

def mag_transform(a, idx, ):
    return 20*np.log10(np.sqrt(a[:,:,0]**2+a[:,:,1]**2))
            

def genModelComparison(dataset: Dataset, benchmark_models: dict, test_metrics: dict, train_test_ratio = 0.7):
    
    """Regression model comparison on Electric Field Dataset. Sklearn predict and fit functions required
        i.e it should work like an sklearn pipeline"""

    train_data, test_data = train_test_data_split(dataset, TRAIN_TEST_RATIO = train_test_ratio)

    train_dataloader = DataLoader(train_data, batch_size = len(train_data))
    test_dataloader = DataLoader(test_data, batch_size = len(test_data))

    TRAIN_PARAMS, TRAIN_FIELDS = next(iter(train_dataloader))
    TEST_PARAMS, TEST_FIELDS = next(iter(test_dataloader))

    df = DataFrame()

    for model_name,model in benchmark_models.items():

        model.fit(TRAIN_PARAMS, TRAIN_FIELDS.reshape(len(TRAIN_FIELDS),-1))

        val_error_list = []
        train_error_list = []

        for test_metric_name,test_metric in test_metrics.items():
            
            train_pred = model.predict(TRAIN_PARAMS).flatten()
            test_pred = model.predict(TEST_PARAMS).flatten()
            train_error_list.append(test_metric(TRAIN_FIELDS.flatten(),train_pred))
            val_error_list.append(test_metric(TEST_FIELDS.flatten(),test_pred))

        df[model_name+ ' Train'] = train_error_list
        df[model_name+ ' Val'] = val_error_list

    df = df.set_axis(list(test_metrics.keys()), axis=0)
    return df



def tensor_conv(a,b):

    pass

