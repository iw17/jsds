import typing as tp, pandas as pd

def import_stats(df: pd.DataFrame, src: str | tp.Iterable[str]) -> None:
    if isinstance(src, str):
        with open(src, 'r') as stats:
            col: str = ''
            while (line := stats.readline().strip()):
                if line.startswith('wk'):
                    col = line
                else:
                    df.loc[df['stu_id'].isin(line.split()), col] = 1
    else: # isinstance(src, Iterable) and not isinstance(src, str)
        for s in src:
            import_stats(df, s)

if __name__ == '__main__':
    cols: list[str] = ['stu_id'] + [f'wk{i}' for i in range(1, 15)]
    df = pd.read_csv('jsds_23sp.csv', usecols=cols)
    df2 = df[(df['stu_id'] >= 'PB21010378') & (df['stu_id'] <= 'PB21010464')]
    for i in range(df2.shape[0]):
        df2.iloc[i, 0] = df2.iloc[i, 0][-3:] # type: ignore
    txts: list[str] = ['jsds_23sp.txt']
    import_stats(df2, txts)
    df2.astype('Int16').fillna(0).to_csv('stats.csv', index=False)
