# Sustainable HPC: Modeling, Characterization, and Implications of Carbon Footprint in Modern HPC Systems

## Paper Result Visualization

### Environment setup

To visualize the results presented in the paper, on a Linux CPU machine, install the necessary Python packages

```
pip install -r requirements.txt
```

### HPC Embodied Carbon

```
cd embodied_carbon
```

The embodied carbon data per HPC component is collected in ``csv/embodied_carbon_by_component.csv``. The embodied carbon is modeled using [ACT](https://github.com/facebookresearch/ACT). The packaging overhead of Seagate SSD/HDDs are modeled using public sustainablity ([Seagate Sustainability](https://www.seagate.com/esg/planet/product-sustainability/)). More details of the embodied carbon modeling process are available in ``csv/embodied_carbon_modeling.xlsx``

The number of devices of individual components from supercomputers are obtained from public resources:

[LUMI](https://events.it4i.cz/event/160/attachments/457/1717/lumi-intro.pdf)
[Perlmutter](https://docs.nersc.gov/systems/perlmutter/architecture/)
[Frontier](https://olcf.ornl.gov/wp-content/uploads/Frontiers-Architecture-Frontier-Training-Series-final.pdf)

The visualization scripts are provided in ``figure_<topic>.ipynb`` files. 

### Regional Operational Carbon

```
cd ../regional_operational_carbon
```

The regional carbon intensity data are collected in the ``csv`` directory. The ``regional_carbon.ipynb`` notebook shows the visualization of regional carbon intensities.

### Combined Carbon

```
cd ../combined_carbon
```

The visualization of hardware upgrade impact on carbon saving are in ``part1.ipynb`` and ``part2.ipynb``