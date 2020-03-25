
    def _to_numpy(self, obj, arg_name):
        arr = None
        if isinstance(obj, np.ndarray):
            arr = obj.copy()
        elif hasattr(obj, 'to_numpy'): # For pandas series.
            arr = obj.to_numpy(copy = True)
        else:
            try:
                arr = np.asarray(obj) # Implicit copying. 
            except Exception:
                text = """
{} cannot be cast into a numpy.ndarray instance.
""".format(arg_name)
                raise TypeError(text.strip())
        # np.ravel(arr)
        return arr
