import numpy as np
from openvino.runtime import Core, Type, Shape, Model, Output, opset10 as ops
import logging
import argparse
import sys
import time


# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def create_dummy_model():
    # Create a simple model that multiplies its input by 2
    input_shape = [1, 224, 224, 3]
    input = ops.parameter(input_shape, Type.f32)
    constant = ops.constant(2, Type.f32)
    result = ops.multiply(input, constant)
    model = Model(result, [input], "dummy_model")
    return model, input_shape

def load_model(core, model_path):
    logger.info(f"Loading model from {model_path}")
    return core.read_model(model_path)

def main():
    parser = argparse.ArgumentParser(description="OpenVINO sample program")
    parser.add_argument("--device", choices=["CPU", "GPU"], default="GPU", help="Specify the device to run on (CPU or GPU)")
    parser.add_argument("--model", help="Path to the model file (.xml)")
    parser.add_argument("--num", type=int, help="number of inference to run")
    args = parser.parse_args()

    logger.info("Starting OpenVINO sample program")

    # Initialize OpenVINO Runtime Core
    core = Core()
    logger.info(f"Available devices: {core.available_devices}")

    # Load model or create dummy model
    if args.model:
        model = load_model(core, args.model)
        input_layer = model.input(0)
        input_shape = input_layer.shape
        num = 100
    else:
        logger.info("No model specified, creating dummy model")
        model, input_shape = create_dummy_model()
        num = 1000

    if args.num:
        num = args.num

    # Compile the model for the specified device
    logger.info(f"Compiling model for {args.device}, shape {input_shape}")
    compiled_model = core.compile_model(model, args.device)

    # Create a random input tensor (adjust shape if needed)
    input_tensor = np.random.random(input_shape).astype(np.float32)

    logger.info(f"Start Inference {num}")
    start_time = time.time()
    for _ in range(num):
        results = compiled_model(input_tensor)
    end_time = time.time()

    logger.info(f"Inference completed in {end_time - start_time:.2f}s successfully")

if __name__ == "__main__":
    main()

