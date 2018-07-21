using Microsoft.WindowsAzure.MobileServices;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tabs.Model;

namespace Tabs
{
    public class AzureManager
    {

        private static AzureManager instance;
        private MobileServiceClient client;
        private IMobileServiceTable<IsChickenModel> isChickenTable;

        private AzureManager()
        {
            this.client = new MobileServiceClient("http://ischicken.azurewebsites.net/");
            this.isChickenTable = this.client.GetTable<IsChickenModel>();
        }

        public MobileServiceClient AzureClient
        {
            get { return client; }
        }

        public static AzureManager AzureManagerInstance
        {
            get
            {
                if (instance == null)
                {
                    instance = new AzureManager();
                }

                return instance;
            }
        }

        public async Task<List<IsChickenModel>> GetChickenInformation()
        {
            return await this.isChickenTable.ToListAsync();
        }

        public async Task PostChickenInformation(IsChickenModel isChickenModel)
        {
            await this.isChickenTable.InsertAsync(isChickenModel);
        }
    }
}