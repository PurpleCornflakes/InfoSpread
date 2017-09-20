import numpy as np
cimport numpy as np 

def _info_spread(np.ndarray[np.int32_t, ndim=2] adjlist_m, \
                np.ndarray[np.int32_t, ndim=1] states):  
    cdef int N = adjlist_m.shape[0]
    cdef int change = 0
    cdef float alpha = 0.4
    cdef float p = 0.2
    cdef float lamda = 0.2
    cdef Py_ssize_t n_i,n_j
    cdef np.ndarray[np.int32_t, ndim=1] new_states = states
    
    for n_i in range(N):
        # the node has been removed
        if adjlist_m[n_i,0] == -1:
            continue
        
        # n_i is not 'S'
        if states[n_i] == 2 or states[n_i] == 0:
            continue 
            
        # n_i is 'S'
        for n_j in adjlist_m[n_i,1:]: 
            # !! Discard Padding
            if n_j == -1:
                continue
            # n_j is 'I'
            if states[n_j] == 0:
                # I-->S
                if np.random.random() < alpha*p:
                    new_states[n_j] = 1
                    change += 1
                # I-->R
                elif np.random.random() < alpha*(1-p):
                    new_states[n_j] = 2
                    change += 1
            # n_j is 'R' or 'S'
            elif np.random.random() < lamda:
                    # S -> R
                    new_states[n_i] = 2
                    change += 1
                    break
            
    return new_states,change