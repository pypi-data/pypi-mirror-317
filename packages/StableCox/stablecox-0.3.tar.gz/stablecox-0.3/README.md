[![DOI](https://zenodo.org/badge/864352564.svg)](https://doi.org/10.5281/zenodo.13852489)

# System Requirements
## Hardware requirements
`Stable Cox' package requires only a standard computer with enough RAM to support the in-memory operations.

## Software requirements
### OS requirements
This package is supported for *Linux*. The package has been tested on the following system:
+ Linux: Ubuntu 18.04

### Python Dependencies
'Stable Cox' mainly depends on the Python scientific stack.

```
lifelines=0.27.8
numpy=1.20.3
pandas=2.0.3
scikit-learn=1.3.0
```

# Run demo

## omics data
# Select topN biomarker and build a predictor on the selected biomarker panel
from StableCox import StableCox
import pandas as pd
training_pd_data = pd.read_csv('./omics_data/HCC_cancer/train_median.csv', index_col=0)

test1_pd_data = pd.read_csv('./omics_data/HCC_cancer/test1_median.csv', index_col=0)

SC = StableCox(alpha=0.0005, hidden_layer_sizes = (98, 11), W_clip=(0.4, 4))

duration_col = "Survival.months"

event_col="Survival.status"

SC.fit(training_pd_data, duration_col, event_col)

cindex = SC.predict_with_topN(test1_pd_data, topN=10)

print("cindex", cindex)


## clinical data
# Make prediction directly without biomarker selection

import pandas as pd
from StableCox import StableCox
training_pd_data = pd.read_csv('./clinical_data/breast_cancer/breast_train_survival.csv', index_col=0)

test1_pd_data = pd.read_csv('./clinical_data/breast_cancer/breast_test1_survival.csv', index_col=0)

training_pd_data = training_pd_data.drop(['Recurr.months', 'Recurr.status', 'Cohort'], axis=1)

test1_pd_data = test1_pd_data.drop(['Recurr.months', 'Recurr.status', 'Cohort'], axis=1)

SC = StableCox(alpha=0.002, hidden_layer_sizes = (69, 15), W_clip=(0.02, 2))

duration_col = "Survival.months"

event_col="Survival.status"

SC.fit(training_pd_data, duration_col, event_col)

cindex = SC.predict(test1_pd_data)

- The expected running time is from several seconds to mins depends on the number of samples.

# License
This project is licensed under the terms of the MIT license.
