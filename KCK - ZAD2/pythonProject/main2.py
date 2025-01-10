import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs


def load_dem(filename):
    with open(filename, 'r') as f:
        width, height, spacing = map(float, f.readline().split())
        data = np.loadtxt(f, skiprows=0)
    return data, width, height, spacing


def calculate_normals(dem_data, spacing):
    gradient_y, gradient_x = np.gradient(dem_data, spacing)
    normals = np.dstack((-gradient_x, gradient_y, np.ones_like(dem_data)))
    return normals

def apply_shading(dem_data, normals, light_vector):
    light_vector = light_vector / np.linalg.norm(light_vector)
    intensity = np.dot(normals, light_vector)
    intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())
    return intensity

def apply_hsv_gradient(data, shading_intensity):
    normalized_data = (data - data.min()) / (data.max() - data.min())
    rgb_image = np.zeros((data.shape[0], data.shape[1], 3))

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            hue = 1/3 * (1 - normalized_data[i, j])
            value = shading_intensity[i, j] * 1.5
            rgb_image[i, j] = cs.hsv_to_rgb(hue, 1, value)

    return rgb_image


dem_data, width, height, spacing = load_dem("C:/Users/kolec/Desktop/KCK - ZAD2/pythonProject/big.dem")
light_vector = np.array([1, 1, 1])
normals = calculate_normals(dem_data, spacing)
shading_intensity = apply_shading(dem_data, normals, light_vector)
color_mapped_data = apply_hsv_gradient(dem_data, shading_intensity)

plt.imshow(color_mapped_data)
plt.savefig("heatmap.pdf")
plt.show()