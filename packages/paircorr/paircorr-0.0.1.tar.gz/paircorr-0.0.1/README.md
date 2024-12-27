# pairplot

```
import pairplot as pp

pp.pairplot_long(df, column, value, index=False)

pp.pairplot_wide(wide_df, column=False)
```


```
import seaborn as sns
import pairplot as pp

iris = sns.load_dataset('iris')

pp.pairplot_wide(iris)
```