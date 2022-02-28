"""
Known errors 
line 43 : RuntimeWarning: overflow encountered in double_scalars 
line 43 : RuntimeWarning: invalid value encountered in double_scalars
"""
import matplotlib.pyplot as plt
from numpy import isinf, isnan

class PID:
    
    def __init__(self, kp=0.31, ki=0.001, kd=0.05):
        
        self.k = {
            "p" : {
                "state": 1,
                "value": kp
            },
            "i" : {
                "state": 1,
                "value": ki
            },
            "d" : {
                "state": 1,
                "value": kd
            },
        }
        self.refernce = [0]
        self.outputs = [0]
        self.errors = [0]
        
    
    def integral_antiwarp(self):        
        if sum(self.errors) !=0 and abs(sum(self.errors[:-2])/sum(self.errors)) < .1:
            return self.errors[:2]
        return self.errors


    def follow(self, refrence_point, timestep=0):
        dt = 0
        self.manage_data()
        while(dt <= timestep):
            self.errors.append(
                self.outputs[-1] - refrence_point
            )
            self.outputs.append(
                self.outputs[-1] - ( \
                    self.k["p"]["state"] * self.k["p"]["value"] * self.errors[-1] + \
                    self.k["i"]["state"] * self.k["i"]["value"] * sum(self.integral_antiwarp()) + \
                    self.k["i"]["state"] * self.k["d"]["value"] * (self.errors[-2]-self.errors[-1])
                    )
                )
            
            self.refernce.append(refrence_point)
            
            if (abs(self.errors[-1])) <= 0.5 :
                break

            if timestep != 0:
                dt = dt+1
    
    def put_data(self):
        return self.refernce, self.outputs, self.errors, [i/100 for i in range(len(self.outputs))]
    
    def manage_data(self):
        if len(self.outputs)>200:
            temp_out = self.outputs[100:]
            self.outputs.clear()
            self.outputs = temp_out.copy()
            del temp_out
        if len(self.errors)>200:
            temp_err = self.errors[100:]
            self.errors.clear()
            self.errors = temp_err.copy()
            del temp_err
        if len(self.refernce)>200:
            temp_ref = self.refernce[100:]
            self.refernce.clear()
            self.refernce = temp_ref.copy()
            del temp_ref
        
            

    
if __name__ == "__main__":
    pid = PID()
    pid.follow(300)
    pid.follow(-100)
    pid.follow(100)
    pid.follow(50)
    pid.follow(0)
    pid.follow(10)
    input, output, err, t = pid.put_data()
    plt.plot(t, input, label='input')
    plt.plot(t, output, label='output')
    plt.legend(loc='best')
    plt.show()
    print(input[-1], output[-1], len(output))
