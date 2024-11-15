from django.shortcuts import render, redirect
from .models import User, Video
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForms, LoginForm, VideoUploadForm, VideoComments
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    videos = Video.objects.all()
    return render(request, 'home.html', {'videos': videos})

def signup(request):
    if request.method == 'POST':
        form = SignUpForms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignUpForms()
    return render(request, 'signup.html', {'form': form})

def login(request):
    # Check if the user is already logged in (session has 'user_id')
    if 'user_id' in request.session:
        messages.info(request, "You are already logged in.")
        return redirect('home')  # Redirect to home page if already logged in

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Try to get the user by email
                user = User.objects.get(email=email)
                
                # Check if the password is correct
                if user.check_password(password):
                    # Set session data to log the user in
                    request.session['user_id'] = user.id  # Store the user ID in session
                    request.session['user_name'] = user.name  # Optional: Store the user's name in session
                    
                    messages.success(request, "Login successful!")
                    return redirect('home')  # Redirect to the home page after successful login
                else:
                    messages.error(request, "Invalid password.")
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout(request):
    # Clear the user's session to log them out
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.info(request, "You have successfully logged out.")
    
    # Redirect to the homepage after logout
    return redirect('home')

def upload_video(request):
    # If the user is not logged in, redirect to login page
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to upload a video.")
        return redirect('login')

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the video with the logged-in user as the uploader
            video = form.save(commit=False)
            video.uploader_id = request.session['user_id']  # Assign the logged-in user as the uploader
            video.save()
            messages.success(request, "Video uploaded successfully!")
            return redirect('home')  # Redirect back to home after successful upload
    else:
        form = VideoUploadForm()

    return render(request, 'upload_video.html', {'form': form})

def video_detail(request, id):
    # Retrieve the video based on its ID or return a 404 if not found
    # Check if the user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view this video.")
        return redirect('login')

    # Retrieve the video based on its ID or return a 404 if not found
    video = Video.objects.get(id=id)
    comments = video.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = VideoComments(request.POST)
        if form.is_valid():
            # Create a new comment but don't save it to the database yet
            comment = form.save(commit=False)
            comment.video = video
            comment.name = request.session.get('user_name')  # Associate the comment with the current video
            comment.save()  # Save the comment
            return redirect('video_detail', id=video.id)  # Redirect to the same page
    else:
        form = VideoComments()
    return render(request, 'video_detail.html', {'video': video, 'comments': comments, 'form': form})

def user_profile(request):
    # Check if the user is logged in
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not logged in

    # Fetch the user from the database using the session's user_id
    user = User.objects.get(id=request.session['user_id'])

    # Fetch the videos uploaded by this user
    uploaded_videos = Video.objects.filter(uploader=user)

    return render(request, 'user_profile.html', {'user': user, 'uploaded_videos': uploaded_videos})

def delete_video(request, video_id):
    # Check if the user is logged in
    if 'user_id' not in request.session:
        return redirect('login')

    # Get the video and check if the logged-in user is the uploader
    video = Video.objects.get(id=video_id, uploader_id=request.session['user_id'])

    # Delete the video
    video.delete()
    messages.success(request, "Video deleted successfully.")
    return redirect('user_profile')

def like_video(request, video_id):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "You must be logged in to like a video.")
        return redirect('login')
    video = Video.objects.get(id=video_id)
    user = User.objects.get(id=user_id)

    # Toggle like status: add like if not liked, remove if already liked
    if user in video.likes.all():
        video.likes.remove(user)
        messages.success(request, "You unliked the video.")
    else:
        video.likes.add(user)
        messages.success(request, "You liked the video.")

    return redirect('video_detail', id=video_id)