# SecondOrder

Data and code for the experiments in

- Dominik Schlechtweg, Cennet Oguz and Sabine Schulte im Walde. 2019. Second-order Co-occurrence Sensitivity of Skip-Gram with Negative Sampling. In *Proceedings of the 2019 ACL Workshop BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP*, Florence, Italy. Association for Computational Linguistics.

If you use this software for academic research, [please cite the paper above](#bibtex) and make sure you give appropriate credit to the below-mentioned software this repository depends on.

The code heavily relies on [DISSECT](http://clic.cimec.unitn.it/composes/toolkit/introduction.html) (modules/composes). We used [hyperwords](https://bitbucket.org/omerlevy/hyperwords) for training PPMI, SVD and SGNS on the extracted word-context pairs.

Usage Note
--------

The scripts should be run directly from the main directory. If you wish to do otherwise, you may have to change the path you add to the path attribute in `sys.path.append('./modules/')` in the scripts. All scripts can be run directly from the command line. To reproduce an artificial corpus similar to the one used in the paper run

	python pair_extraction/simulate_pairs.py 10 1000 1000 ./simul-pairs

In order to extract equally many (1.0) second-order co-occurrence pairs from a small first-order pair sample ignoring words above a (co-occurrence) frequency of 5 run

	python pair_extraction/second_order_pairs.py pairs/test/pairs 1.0 5 pairs/test/second_order_pairs

Regular word-context corpus pairs can be extracted and models can be trained with [hyperwords](https://bitbucket.org/omerlevy/hyperwords). We recommend you to run the scripts with the Python Anaconda distribution (Python 2.7.15). You will have to install some additional packages such as docopt. Those that aren't available from the Anaconda installer can be installed via EasyInstall. Please do not hesitate to write us an email if you need any help or additional scripts or data.

BibTex
--------

```
@inproceedings{Schlechtwegetal19SecondOrder,
    author = "Schlechtweg, D. and Oguz, C. and {Schulte im Walde}, S.",
    title = "Second-order Co-occurrence Sensitivity of Skip-Gram with Negative Sampling",
    booktitle = "Proceedings of the 2019 {ACL} Workshop {B}lackbox{NLP}: Analyzing and Interpreting Neural Networks for {NLP}",
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics"
}
```
