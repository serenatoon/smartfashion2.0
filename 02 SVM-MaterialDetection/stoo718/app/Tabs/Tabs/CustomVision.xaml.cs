using System;
using System.Diagnostics.Contracts;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Plugin.Media;
using Plugin.Media.Abstractions;
using Tabs.Model;
using Xamarin.Forms;
using Plugin.Geolocator;
using System.Globalization;
using System.Text;

namespace Tabs
{
    public partial class CustomVision : ContentPage
    {
        public CustomVision()
        {
            InitializeComponent();
        }

        private async void loadCamera(object sender, EventArgs e)
        {
            await CrossMedia.Current.Initialize();

            if (!CrossMedia.Current.IsCameraAvailable || !CrossMedia.Current.IsTakePhotoSupported)
            {
                await DisplayAlert("No Camera", ":( No camera available.", "OK");
                return;
            }

            MediaFile file = await CrossMedia.Current.TakePhotoAsync(new StoreCameraMediaOptions
            {
                PhotoSize = PhotoSize.Medium,
                Directory = "Sample",
                Name = $"{DateTime.UtcNow}.jpg"
            });

            if (file == null)
                return;

            image.Source = ImageSource.FromStream(() =>
            {
                return file.GetStream();
            });

            TagLabel.Text = "Analysing.......";
            //await postLocationAsync(); // post location 
            await MakePredictionRequest(file);
        }

        async Task postLocationAsync()
        {

            var locator = CrossGeolocator.Current;
            locator.DesiredAccuracy = 50;

            var position = await locator.GetPositionAsync(TimeSpan.FromSeconds(10)); // convert from int to timespan, '1000' doesn't seem to work 

            IsChickenModel model = new IsChickenModel()
            {
                Longitude = (float)position.Longitude,
                Latitude = (float)position.Latitude,
                Timestamp = DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm",
                                       CultureInfo.InvariantCulture)

            };

            await AzureManager.AzureManagerInstance.PostChickenInformation(model);
        }

        static byte[] GetImageAsByteArray(MediaFile file)
        {
            var stream = file.GetStream();
            BinaryReader binaryReader = new BinaryReader(stream);
            return binaryReader.ReadBytes((int)stream.Length);
        }

        public class B64
        {
            public String img_data;

            public B64(String data)
            {
                img_data = data;
            }
        }

        async Task MakePredictionRequest(MediaFile file)
        {
            Contract.Ensures(Contract.Result<Task>() != null);
            //var client = new HttpClient();

            //client.DefaultRequestHeaders.Add("Prediction-Key", "2596b2fb91e34f07b738da9bd906e5ef");

            string url = "http://222.155.102.53:10008/receiveFile?";
            Debug.WriteLine("hi");


            byte[] byteData = GetImageAsByteArray(file);
            String b64_data = Convert.ToBase64String(byteData);
            B64 b64_class = new B64(b64_data);
            var payload = JsonConvert.SerializeObject(b64_class);
            var httpContent = new StringContent(payload, Encoding.UTF8, "application/json");

            using (var httpClient = new HttpClient())
            {

                //content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
                try
                {
                    await httpClient.PostAsync(url, null);
                    var response = await httpClient.PostAsync(url, httpContent);
                    if (response.Content != null)
                    {
                        var responseContent = await response.Content.ReadAsStringAsync();
                    }
                }
                catch (Exception ex)
                {
                    throw new Exception("Unknown Exception Thrown: "
                       + "\n  Type:    " + ex.GetType().Name
                       + "\n  Message: " + ex.Message);
                }
                Debug.WriteLine("making request....");




                //Get rid of file once we have finished using it
                file.Dispose();
            }
        }
    }
}
