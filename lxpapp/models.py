from django.db import models
from django.urls import reverse
from social_django import models as UMODEL
from django.contrib.auth.models import User
import datetime
from django.db.models import Q, Sum
import requests
import humanize
from django.db import models

class UserPics(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    picpath = models.TextField(default='')
    pic = models.ImageField()
###################################
def getHumanizedTimeString(seconds):
      
      return humanize.precisedelta(
         datetime.timedelta(seconds=seconds)).upper(). \
         replace(" month".upper(), "m.").replace(" months".upper(), "m.").replace(" days".upper(), "d.").replace(
         " day".upper(), "d.").replace(" hours".upper(), "hrs.").replace(" hour".upper(), "hr.").replace(
         " minutes".upper(), "mins.").replace(" minute".upper(), "min.").replace(
         "and".upper(), "").replace(" seconds".upper(), "secs.").replace(" second".upper(), "sec.").replace(",", "")

SECRETS = {"SECRET_KEY": 'django-insecure-ycs22y+20sq67y(6dm6ynqw=dlhg!)%vuqpd@$p6rf3!#1h$u=',
           "YOUTUBE_V3_API_KEY": 'AIzaSyCBOucAIJ5PdLeqzTfkTQ_6twsjNaMecS8',
           "GOOGLE_OAUTH_CLIENT_ID": "699466001074-biu4pjifnphoh1raipgi5mm5bf72h1ot.apps.googleusercontent.com",
           "GOOGLE_OAUTH_CLIENT_SECRET": "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",
           "GOOGLE_OAUTH_SCOPES": ['https://www.googleapis.com/auth/youtube']}
class Tag(models.Model):
    name = models.CharField(max_length=69)
    created_by = models.ForeignKey(User, related_name="playlist_tags", on_delete=models.CASCADE, null=True)

    times_viewed = models.IntegerField(default=0)
    times_viewed_per_week = models.IntegerField(default=0)
    # type = models.CharField(max_length=10)  # either 'playlist' or 'video'

    last_views_reset = models.DateTimeField(default=datetime.datetime.now)

class Video(models.Model):
    # video details
    video_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    duration_in_seconds = models.BigIntegerField(default=0)
    thumbnail_url = models.TextField(blank=True)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField(default="")
    has_cc = models.BooleanField(default=False, blank=True, null=True)
    liked = models.BooleanField(default=False)  # whether this video liked on YouTube by user or not

    # video stats
    public_stats_viewable = models.BooleanField(default=True)
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    dislike_count = models.BigIntegerField(default=0)
    comment_count = models.BigIntegerField(default=0)

    yt_player_HTML = models.TextField(blank=True)

    # video is made by this channel
    # channel = models.ForeignKey(Channel, related_name="videos", on_delete=models.CASCADE)
    channel_id = models.TextField(blank=True)
    channel_name = models.TextField(blank=True)

    # which playlist this video belongs to, and position of that video in the playlist (i.e ALL videos belong to some pl)
    # playlist = models.ForeignKey(Playlist, related_name="videos", on_delete=models.CASCADE)

    # (moved to playlistItem)
    # is_duplicate = models.BooleanField(default=False)  # True if the same video exists more than once in the playlist
    # video_position = models.IntegerField(blank=True)

    # NOTE: For a video in db:
    # 1.) if both is_unavailable_on_yt and was_deleted_on_yt are true,
    # that means the video was originally fine, but then went unavailable when updatePlaylist happened
    # 2.) if only is_unavailable_on_yt is true and was_deleted_on_yt is false,
    # then that means the video was an unavaiable video when initPlaylist was happening
    # 3.) if both is_unavailable_on_yt and was_deleted_on_yt are false, the video is fine, ie up on Youtube
    is_unavailable_on_yt = models.BooleanField(
        default=False)  # True if the video was unavailable (private/deleted) when the API call was first made
    was_deleted_on_yt = models.BooleanField(default=False)  # True if video became unavailable on a subsequent API call

    is_planned_to_watch = models.BooleanField(default=False)  # mark video as plan to watch later
    is_marked_as_watched = models.BooleanField(default=False)  # mark video as watched
    is_favorite = models.BooleanField(default=False, blank=True)  # mark video as favorite
    num_of_accesses = models.IntegerField(default=0)  # tracks num of times this video was clicked on by user
    user_label = models.CharField(max_length=100, blank=True)  # custom user given name for this video
    user_notes = models.TextField(blank=True)  # user can take notes on the video and save them

    # for new videos added/modified/deleted in the playlist
    video_details_modified = models.BooleanField(
        default=False)  # is true for videos whose details changed after playlist update
    def __str__(self):
        return str(self.name)

class Playlist(models.Model):
    tags = models.ManyToManyField(Tag, related_name="playlists")
    # playlist is made by this channel
    channel_id = models.TextField(blank=True)
    channel_name = models.TextField(blank=True)

    # playlist details
    is_yt_mix = models.BooleanField(default=False)
    playlist_id = models.CharField(max_length=150)
    name = models.CharField(max_length=150, blank=True)  # YT PLAYLIST NAMES CAN ONLY HAVE MAX OF 150 CHARS
    thumbnail_url = models.TextField(blank=True)
    description = models.TextField(default="No description")
    video_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    is_private_on_yt = models.BooleanField(default=False)
    videos = models.ManyToManyField(Video, related_name="playlists")

    # eg. "<iframe width=\"640\" height=\"360\" src=\"http://www.youtube.com/embed/videoseries?list=PLFuZstFnF1jFwMDffUhV81h0xeff0TXzm\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>"
    playlist_yt_player_HTML = models.TextField(blank=True)

    playlist_duration = models.CharField(max_length=69, blank=True)  # string version of playlist dureation
    playlist_duration_in_seconds = models.BigIntegerField(default=0)

    # watch playlist details
    # watch_time_left = models.CharField(max_length=150, default="")
    started_on = models.DateTimeField(default=datetime.datetime.now, null=True)
    last_watched = models.DateTimeField(default=datetime.datetime.now, null=True)

    # manage playlist
    user_notes = models.TextField(default="")  # user can take notes on the playlist and save them
    user_label = models.CharField(max_length=100, default="")  # custom user given name for this playlist
    marked_as = models.CharField(default="none",
                                 max_length=100)  # can be set to "none", "watching", "on-hold", "plan-to-watch"
    is_favorite = models.BooleanField(default=False, blank=True)  # to mark playlist as fav
    num_of_accesses = models.IntegerField(default="0")  # tracks num of times this playlist was opened by user
    last_accessed_on = models.DateTimeField(default=datetime.datetime.now)
    is_user_owned = models.BooleanField(default=True)  # represents YouTube playlist owned by user

    # set playlist manager
    #objects = PlaylistManager()

    # playlist settings (moved to global preferences)
    # hide_unavailable_videos = models.BooleanField(default=False)
    # confirm_before_deleting = models.BooleanField(default=True)
    auto_check_for_updates = models.BooleanField(default=False)

    # for import
    is_in_db = models.BooleanField(default=False)  # is true when all the videos of a playlist have been imported
    
    # for updates
    has_playlist_changed = models.BooleanField(default=False)  # determines whether playlist was modified online or not
    has_new_updates = models.BooleanField(default=False)  # meant to keep track of newly added/unavailable videos

    def __str__(self):
        return str(self.name)

    def has_unavailable_videos(self):
        if self.playlist_items.filter(Q(video__is_unavailable_on_yt=True) & Q(video__was_deleted_on_yt=False)).exists():
            return True
        return False

    def has_duplicate_videos(self):
        if self.playlist_items.filter(is_duplicate=True).exists():
            return True
        return False

    def get_channels_list(self):
        channels_list = []
        num_channels = 0
        for video in self.videos.all():
            channel = video.channel_name
            if channel not in channels_list:
                channels_list.append(channel)
                num_channels += 1

        return [num_channels, channels_list]

    def generate_playlist_thumbnail_url(self):
        """
        Generates a playlist thumnail url based on the playlist name
        """
        
        pl_name = self.name
        response = requests.get(
            f'https://api.unsplash.com/search/photos/?client_id={SECRETS["UNSPLASH_API_ACCESS_KEY"]}&page=1&query={pl_name}')
        image = response.json()["results"][0]["urls"]["small"]

        print(image)

        return image

    def get_playlist_thumbnail_url(self):
        playlist_items = self.playlist_items.filter(
            Q(video__was_deleted_on_yt=False) & Q(video__is_unavailable_on_yt=False))
        if playlist_items.exists():
            return playlist_items.first().video.thumbnail_url
        else:
            return "https://i.ytimg.com/vi/9219YrnwDXE/maxresdefault.jpg"

    def get_unavailable_videos_count(self):
        return self.video_count - self.get_watchable_videos_count()

    def get_duplicate_videos_count(self):
        return self.playlist_items.filter(is_duplicate=True).count()

    # return count of watchable videos, i.e # videos that are not private or deleted in the playlist
    def get_watchable_videos_count(self):
        return self.playlist_items.filter(
            Q(is_duplicate=False) & Q(video__is_unavailable_on_yt=False) & Q(video__was_deleted_on_yt=False)).count()

    def get_watched_videos_count(self):
        return self.playlist_items.filter(Q(is_duplicate=False) &
                                          Q(video__is_marked_as_watched=True) & Q(
            video__is_unavailable_on_yt=False) & Q(video__was_deleted_on_yt=False)).count()

    # diff of time from when playlist was first marked as watched and playlist reached 100% completion
    def get_finish_time(self):
        return self.last_watched - self.started_on

    

    def get_watch_time_left(self):
        unwatched_playlist_items_secs = self.playlist_items.filter(Q(is_duplicate=False) &
                                                                   Q(video__is_marked_as_watched=False) &
                                                                   Q(video__is_unavailable_on_yt=False) &
                                                                   Q(video__was_deleted_on_yt=False)).aggregate(
            Sum('video__duration_in_seconds'))['video__duration_in_seconds__sum']

        watch_time_left =  getHumanizedTimeString(
            unwatched_playlist_items_secs) if unwatched_playlist_items_secs is not None else getHumanizedTimeString(0)

        return watch_time_left

    # return 0 if playlist empty or all videos in playlist are unavailable
    def get_percent_complete(self):
        total_playlist_video_count = self.get_watchable_videos_count()
        watched_videos = self.playlist_items.filter(Q(is_duplicate=False) &
                                                    Q(video__is_marked_as_watched=True) & Q(
            video__is_unavailable_on_yt=False) & Q(video__was_deleted_on_yt=False))
        num_videos_watched = watched_videos.count()
        percent_complete = round((num_videos_watched / total_playlist_video_count) * 100,
                                 1) if total_playlist_video_count != 0 else 0
        return percent_complete

    def all_videos_unavailable(self):
        all_vids_unavailable = False
        if self.videos.filter(
                Q(is_unavailable_on_yt=True) | Q(was_deleted_on_yt=True)).count() == self.video_count:
            all_vids_unavailable = True
        return all_vids_unavailable


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, related_name="playlist_items",
                                 on_delete=models.CASCADE, null=True)  # playlist this pl item belongs to
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)

    # details
    playlist_item_id = models.CharField(max_length=100)  # the item id of the playlist this video beo
    video_position = models.IntegerField(blank=True)  # video position in the playlist
    published_at = models.DateTimeField(default=datetime.datetime.now)  # snippet.publishedAt - The date and time that the item was added to the playlist
    channel_id = models.CharField(null=True,
                                  max_length=250)  # snippet.channelId - The ID that YouTube uses to uniquely identify the user that added the item to the playlist.
    channel_name = models.CharField(null=True,
                                    max_length=250)  # snippet.channelTitle -  The channel title of the channel that the playlist item belongs to.

    # video_owner_channel_id = models.CharField(max_length=100)
    # video_owner_channel_title = models.CharField(max_length=100)
    is_duplicate = models.BooleanField(default=False)  # True if the same video exists more than once in the playlist
    is_marked_as_watched = models.BooleanField(default=False, blank=True)  # mark video as watched
    num_of_accesses = models.IntegerField(default=0)  # tracks num of times this video was clicked on by user

    # for new videos added/modified/deleted in the playlist
    # video_details_modified = models.BooleanField(
    #    default=False)  # is true for videos whose details changed after playlist update
    # video_details_modified_at = models.DateTimeField(default=datetime.datetime.now)  # to set the above false after a day
   

class Pin(models.Model):
    kind = models.CharField(max_length=100)  # "playlist", "video"
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)

##############################################################################

class Topic(models.Model):
    chapter=models.ForeignKey(Video,on_delete=models.SET_NULL, null=True, blank=True)
    subject=models.ForeignKey(Playlist,on_delete=models.SET_NULL, null=True, blank=True)
    topic_name = models.CharField(max_length=50)
    def __str__(self):
        return self.topic_name

class Course(models.Model):
   course_name = models.CharField(max_length=50)
   def __str__(self):
    return self.course_name
   
   def get_absolute_url(self):
        return reverse('course-update', kwargs={'pk': self.pk})

class CourseDetails(models.Model):
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   subject=models.ForeignKey(Playlist,on_delete=models.CASCADE)
   chapter=models.ForeignKey(Video,on_delete=models.CASCADE)
   topic=models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True, blank=True)

class UserCourse(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   remarks = models.CharField(max_length=50)

class CourseType(models.Model):
   coursetype_name = models.CharField(max_length=50)
   def __str__(self):
      return self.coursetype_name

class Batch(models.Model):
   batch_name = models.CharField(max_length=50)
   coursetype=models.ForeignKey(CourseType,on_delete=models.CASCADE)
   fee = models.IntegerField(default=0)
   stdate = models.DateField()
   enddate = models.DateField()
   def __str__(self):
      return self.batch_name

class BatchTrainer(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
   trainer=models.ForeignKey(User,on_delete=models.CASCADE)

class Batchlearner(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
   learner=models.ForeignKey(User,on_delete=models.CASCADE)
 
class PassionateSkill(models.Model):
   passionateskill_name = models.CharField(max_length=200)
   def __str__(self):
        return self.passionateskill_name

class KnownSkill(models.Model):
   knownskill_name = models.CharField(max_length=200)
   def __str__(self):
        return self.knownskill_name

class LearnerDetails(models.Model):
    learner=models.ForeignKey(User,on_delete=models.CASCADE)
    user_full_name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    iswhatsapp = models.BooleanField(default=False)
    whatsappno = models.IntegerField(default=0)
    
class LearnerDetailsPSkill(models.Model):
    learnerdetails=models.ForeignKey(LearnerDetails,on_delete=models.CASCADE)
    passionateskill=models.ForeignKey(PassionateSkill,on_delete=models.CASCADE)

class LearnerDetailsKSkill(models.Model):
    learnerdetails=models.ForeignKey(LearnerDetails,on_delete=models.CASCADE)
    knownskill=models.ForeignKey(KnownSkill,on_delete=models.CASCADE)

class IsFirstLogIn(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user


class Exam(models.Model):
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
   exam_name = models.CharField(max_length=50)
   cat=(('MCQ','MCQ'),('ShortAnswer','ShortAnswer'))
   questiontpye=models.CharField(max_length=200,choices=cat,default='')
   def __str__(self):
        return self.exam_name

class McqQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=0)

class McqResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class McqResultDetails(models.Model):
    mcqresult=models.ForeignKey(McqResult,on_delete=models.CASCADE)
    question = models.ForeignKey(McqQuestion,on_delete=models.CASCADE)
    selected=models.CharField(max_length=200)

class ShortQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
   question=models.CharField(max_length=600)
   marks=models.IntegerField(default=0)

class ShortResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    datecreate = models.DateTimeField(auto_now=True)
    status= models.BooleanField(default=False)
    timetaken = models.CharField(max_length=200)

class ShortResultDetails(models.Model):
    shortresult=models.ForeignKey(ShortResult,on_delete=models.CASCADE)
    question=models.ForeignKey(ShortQuestion,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    answer=models.CharField(max_length=200)
    feedback=models.CharField(max_length=200,default='')
   
class VideoTopicCount(models.Model):
   video=models.ForeignKey(Video,on_delete=models.CASCADE)
   TopicCovered=models.PositiveIntegerField(default=0)

class VideoTimeLine(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    learner_id=models.PositiveIntegerField(default=0)
    TopicName=models.CharField(max_length=600)
    VideoTime=models.CharField(max_length=600)
    cat=(('Approved','Approved'),('Rejected','Rejected'),('Pending','Pending'))
    status=models.CharField(max_length=200,choices=cat, default= 'Pending')

class VideoToUnlock(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    learner=models.ForeignKey(User,on_delete=models.CASCADE)

class VideoWatched(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    learner=models.ForeignKey(User,on_delete=models.CASCADE)

class WaringMail(models.Model):
    learner=models.ForeignKey(User,on_delete=models.CASCADE)
    usermailid=models.TextField()
    mailed=models.TextField()
    totvideo = models.IntegerField(default=0)
    watched = models.IntegerField(default=0)
    watchedperc = models.DecimalField(max_digits=5, decimal_places=2)
    pending = models.IntegerField(default=0)
    datetimestamp = models.DateTimeField()

class Material(models.Model):
    subject=models.ForeignKey(Playlist,on_delete=models.CASCADE)
    chapter=models.ForeignKey(Video,on_delete=models.CASCADE)
    mtype=models.PositiveIntegerField(default=0)
    urlvalue=models.TextField()
    description=models.TextField()

class K8STerminal(models.Model):
    trainer=models.ForeignKey(User,on_delete=models.CASCADE, related_name='%(class)s_requests_trainer')
    learner=models.ForeignKey(User,on_delete=models.CASCADE, related_name='%(class)s_requests_learner')
    Password=models.TextField()
    usagevalue=models.PositiveIntegerField(default=0)

class K8STerminalLearnerCount(models.Model):
    learner=models.ForeignKey(User,on_delete=models.CASCADE)
    usedvalue=models.PositiveIntegerField(default=0)


class CrudUser(models.Model):
    name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)

class LiveSession(models.Model):
    trainer=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.ForeignKey(Playlist,on_delete=models.CASCADE)
    password = models.CharField(max_length=30, blank=True)

class LiveQuestion(models.Model):
    livesession=models.ForeignKey(LiveSession,on_delete=models.CASCADE)
    question = models.CharField(max_length=500, blank=True)

class LiveSessionUsers(models.Model):
    livesession=models.ForeignKey(LiveSession,on_delete=models.CASCADE)
    livequestion=models.ForeignKey(LiveQuestion,on_delete=models.CASCADE)
    answer = models.CharField(max_length=500, blank=True)
    correct = models.BooleanField(default=0)

