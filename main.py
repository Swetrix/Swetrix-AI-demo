from fastapi import FastAPI
from API.models import ChartData
from API.serializers import Serializer
from Prediction.enums import Frequency
from Prediction.model import Model
from Prediction.process_data import Data
from fastapi.responses import Response

app = FastAPI()


@app.middleware("http")
async def add_cors_headers(request, call_next):
    if request.method == "OPTIONS":
        return Response(status_code=204)

    response = await call_next(request)
    return response


@app.post("/")
async def get_data(request_data: ChartData):
    # Get data from request and convert it to the right format
    period_to_forecast = request_data.period_to_forecast
    frequency = Frequency.get_frequency(request_data.frequency)

    # Convert to pandas dataframe
    pd_data = request_data.to_pandas()

    # Process data
    data = Data(original_data=pd_data)
    all_dataframes = data.generate_dataframes()

    # The list of serialized data which will be returned to the client
    serialized_list = []

    # Train model for each field we want to forecast
    for df, field in zip(all_dataframes, request_data.keys()):
        print(field)
        model = Model(df, period_to_forecast, frequency)
        forecasted_data = model.train()
        print(forecasted_data)
        ser = Serializer(frequency=frequency, field=field)
        ser.append_for_period(field, forecasted_data)
        serialized_list.append(ser.serialized_data)

    processed_data = Serializer.remove_duplicates(serialized_list)

    return processed_data
