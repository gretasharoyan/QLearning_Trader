 	   		  	  			  		 			     			  	 
import random as rand  		  	   		  	  			  		 			     			  	   		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
class QLearner(object):  		  	   		  	  			  		 			     			  	 
	  	   		  	  			  		 			     			  	 
    def __init__(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        num_states=100,  		  	   		  	  			  		 			     			  	 
        num_actions=4,  		  	   		  	  			  		 			     			  	 
        alpha=0.2,  		  	   		  	  			  		 			     			  	 
        gamma=0.9,  		  	   		  	  			  		 			     			  	 
        rar=0.5,  		  	   		  	  			  		 			     			  	 
        radr=0.99,  		  	   		  	  			  		 			     			  	 
        dyna=0,  		  	   		  	  			  		 			     			  	 
        verbose=False,  		  	   		  	  			  		 			     			  	 
    ):  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        self.verbose = verbose  		  	   		  	  			  		 			     			  	 
        self.num_actions = num_actions  		  	   		  	  			  		 			     			  	 
        self.s = 0  		  	   		  	  			  		 			     			  	 
        self.a = 0  
        self.rar = rar
        self.radr = radr
        self.alpha = alpha	
        self.gamma = gamma
        self.dyna = dyna
        self.dyna_arr = np.empty((0, 4))
        self.table = np.zeros([num_states, num_actions])	  
    
  	  			  		 			     			  	 
    def querysetstate(self, s):  		  	   		  	  			  		 			     			  	 
	  	   		  	  			  		 			     			  	 
        self.s = s  		  	   		  	  			  		 			     			  	 
                
        if rand.uniform(0.0, 1.0) <= self.rar and self.rar!=0:

            action = rand.randint(0, self.num_actions - 1)
            self.a = action
            if self.verbose:  		  	   		  	  			  		 			     			  	 
                print(f"s = {s}, a = {action}")  	
            return action 	
        
        action = self.table[s].argmax()  
        self.a = action      	  	   		  	  			  		 			     			  	 
        if self.verbose:  		  	   		  	  			  		 			     			  	 
            print(f"s = {s}, a = {action}")  		  	   		  	  			  		 			     			  	 
        return action  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    def query(self, s_prime, r):  		  	   		  	  			  		 			     			  	 
		  	   		  	  			  		 			     			  	 
        action = rand.randint(0, self.num_actions - 1) 
        arg_max = self.table[s_prime].argmax() 
        self.table[self.s, self.a] = (1 - self.alpha)*self.table[self.s, self.a] + self.alpha*(r + self.gamma*self.table[s_prime, arg_max ])
 
        
        if self.dyna>0:
            self.dyna_arr = np.append(self.dyna_arr, np.array([[self.s, self.a, s_prime, r]]), axis = 0)
            if len(self.dyna_arr)<self.dyna:
                count = len(self.dyna_arr)
            else:
                count = self.dyna
            for i in range(count):
                int_rand = rand.randint(0, len(self.dyna_arr) -1 )
                dyna_row = self.dyna_arr[int_rand]
                arg_max_dyna = self.table[int(dyna_row[2])].argmax() 
                self.table[int(dyna_row[0]), int(dyna_row[1])] = (1 - self.alpha)*self.table[int(dyna_row[0]), int(dyna_row[1])] + self.alpha*(dyna_row[3] + self.gamma*self.table[int(dyna_row[2]), arg_max_dyna ])



        self.s = s_prime    
        if rand.uniform(0.0, 1.0) <= self.rar:
            self.rar *= self.radr	
            action = rand.randint(0, self.num_actions - 1)
            self.a = action
            if self.verbose:  		  	   		  	  			  		 			     			  	 
                print(f"s = {s_prime}, a = {action}, r={r}")  	
            return action 	
        self.rar *= self.radr	  	   		  	  			  		 			     			  	 
        if self.verbose:  		  	   		  	  			  		 			     			  	 
            print(f"s = {s_prime}, a = {arg_max}, r={r}")  	
        # action = self.table[s_prime].argmax()  
        arg_max = self.table[s_prime].argmax() 
        self.a = arg_max 	  	   		  	  			  		 			     			  	 
        return arg_max   		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 