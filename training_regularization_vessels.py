from Adjoint_regularizition import Regularized
import Operators.Load_PAT2D_data as PATdata
import platform
from Framework import approx_PAT_matrix as ApproxPAT
from Framework import exact_PAT_operator as ExactPAT

if platform.node() == 'motel':
    prefix = '/local/scratch/public/sl767/ModelCorrection/'
else:
    prefix = ''

matrix_path = prefix+'Data/Matrices/threshSingleMatrix4Py.mat'
data_path = prefix+'Data/vessels/'
saves_path = prefix+'Saves/vessels/'

print(saves_path)
print(data_path)

train_append = 'vesselBatch2D_train.mat'
test_append = 'vesselBatch2D_test.mat'
data_sets = PATdata.read_data_sets(data_path + train_append, data_path + test_append, vessels=True)

INPUT_DIM = (64,64)
OUTPUT_DIM = (64,64)

approx = ApproxPAT(matrix_path=matrix_path, input_dim=INPUT_DIM, output_dim=OUTPUT_DIM)
exact = ExactPAT(matrix_path=matrix_path, input_dim=INPUT_DIM, output_dim=OUTPUT_DIM)


lam = 0.001


if 1:
    correction = Regularized(path=saves_path, true_np=exact, appr_np=approx, lam=lam, data_sets=data_sets,
                             experiment_name='RegularizedAdjoint')

    rate = 5e-5
    recursions = 1
    step_size = 0.0
    iterations = 2

    for i in range(iterations):
        for k in range(1000):
            correction.train(recursions, step_size, learning_rate=rate)
            if k % 50 == 0:
                correction.log(recursions, step_size)
        # recursions = recursions+1
    correction.save()

if 0:
    correction = Regularized(path=saves_path, true_np=exact, appr_np=approx, lam=lam, data_sets=data_sets,
                             experiment_name='RegularizedAdjointRekursive')
    rate = 5e-4
    recursions_max = 100
    step_size = 0.1
    iterations = 10

    if 1:
        for i in range(iterations):
            recursions = int((recursions_max * i / (iterations - 1)) + 1)
            print(recursions)
            for k in range(300):
                correction.train(recursions, step_size, learning_rate=rate)
                if k % 20 == 0:
                    correction.log(recursions, step_size)
            # recursions = recursions+1
            correction.save()


correction.log_optimization(recursions=100, step_size=step_size, lam=0.0)
correction.log_gt_optimization(recursions=100, step_size=step_size, lam=0.0)
correction.log_approx_optimization(recursions=100, step_size=step_size, lam=0.0)

correction.log_optimization(recursions=100, step_size=step_size, lam=lam)
correction.log_gt_optimization(recursions=100, step_size=step_size, lam=lam)
correction.log_approx_optimization(recursions=100, step_size=step_size, lam=lam)


correction.end()


