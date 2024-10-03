import vtk

# Read and display a 2D image

# Create reader
reader = vtk.vtkJPEGReader()
reader.SetFileName("image-manipulator-python/LegoDarkFalcon.jpg")

# Verify image file
if not reader.CanReadFile("image-manipulator-python/LegoDarkFalcon.jpg"):
    print("Image read failed")
    exit()

# Create image viewer
image_viewer = vtk.vtkImageViewer2()
image_viewer.SetInputConnection(reader.GetOutputPort())


# Create render window
render_window = vtk.vtkRenderWindow()
image_viewer.SetRenderWindow(render_window)
render_window.SetSize(800,600)

# Create a render window interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
image_viewer.SetupInteractor(render_window_interactor)

# Render the image
image_viewer.Render()
image_viewer.GetRenderer().ResetCamera()

rotation_angle = 0

def rotate_image(direction):
    global rotation_angle
    rotation_angle += direction * 10
    image_dimensionas = reader.GetOutput().GetDimensions()
    centerX = image_dimensionas[0] / 2
    centerY = image_dimensionas[1] / 2

    transform = vtk.vtkTransform()
    transform.Translate(centerX, centerY, 0)
    transform.RotateZ(rotation_angle)
    transform.Translate(-centerX, -centerY, 0)  # Move back

    image_viewer.GetImageActor().SetUserTransform(transform)
    render_window.Render()


# Key press event handler
def event_handler(obj, event):
    key = obj.GetKeySym()

    if key == 'q': # Exit
        render_window_interactor.GetRenderWindow().Finalize()
        render_window_interactor.GetRenderWindow().SetWindowName("Exiting...")
        render_window_interactor.TerminateApp()
    elif key == 'd': # Rotate clockwise
        rotate_image(-1)
    elif key == 'a': # Rotate counterclockwise
        rotate_image(1)


render_window_interactor.AddObserver("KeyPressEvent", event_handler)

# Start interaction
render_window_interactor.Start()