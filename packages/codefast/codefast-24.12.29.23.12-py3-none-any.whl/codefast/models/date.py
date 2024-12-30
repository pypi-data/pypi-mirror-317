import httpx
import pydantic

API_URL = 'https://www.worldtimeapi.org/api/timezone/'


class RealDate(pydantic.BaseModel):
    date: str
    time: str
    day_of_week: int
    day_of_month: int
    day_of_year: int
    week_number: int
    unix_timestamp: int

    @property
    def year(self) -> int:
        return int(self.date.split('-')[0])

    @property
    def month(self) -> int:
        return int(self.date.split('-')[1])

    @property
    def day(self) -> int:
        return self.day_of_month

    @pydantic.model_serializer(mode='plain')
    def serialize(self):
        return {
            'date': self.date,
            'time': self.time,
            'day_of_week': self.day_of_week,
            'day_of_month': self.day_of_month,
            'day_of_year': self.day_of_year,
            'week_number': self.week_number,
            'unix_timestamp': self.unix_timestamp,
            'year': self.year,
            'month': self.month,
            'day': self.day
        }


async def arealdate(timezone: str = 'Asia/Shanghai') -> RealDate:
    # Use async HTTP client for non-blocking requests
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/{timezone}")
        data = response.json()
        date_str = data['datetime'].split('T')[0]
        time_str = data['datetime'].split('T')[1].split('.')[0]

        return RealDate(date=date_str,
                        time=time_str,
                        day_of_week=data['day_of_week'],
                        day_of_month=int(date_str.split('-')[2]),
                        day_of_year=data['day_of_year'],
                        week_number=data['week_number'],
                        unix_timestamp=data['unixtime'])


def realdate(timezone: str = 'Asia/Shanghai') -> RealDate:
    # Synchronous version using blocking HTTP request
    response = httpx.get(f"{API_URL}/{timezone}")
    data = response.json()

    # Extract date from datetime string
    date_str = data['datetime'].split('T')[0]
    time_str = data['datetime'].split('T')[1].split('.')[0]

    return RealDate(date=date_str,
                    time=time_str,
                    day_of_week=data['day_of_week'],
                    day_of_month=int(date_str.split('-')[2]),
                    day_of_year=data['day_of_year'],
                    week_number=data['week_number'],
                    unix_timestamp=data['unixtime'])


if __name__ == '__main__':
    rd = realdate()
    print(rd.model_dump_json())
