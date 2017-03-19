from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService
import ydk.models.openconfig.openconfig_telemetry as oc_telemetry
import urllib

HOST = '10.71.158.139'
PORT = 830
USER = 'cisco'
PASS = 'cisco'

xr = NetconfServiceProvider(address=HOST,
	port=PORT,
	username=USER,
	password=PASS,
	protocol = 'ssh')

# Sensor Group

sgroup = oc_telemetry.TelemetrySystem.SensorGroups.SensorGroup()
sgroup.sensor_group_id="SGroup3"
sgroup.config.sensor_group_id="SGroup3"

sgroup.sensor_paths = sgroup.SensorPaths()
new_sensorpath = sgroup.SensorPaths.SensorPath()

interface_stats_path = urllib.quote('Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters', safe=':')
new_sensorpath.path = interface_stats_path
new_sensorpath.config.path = interface_stats_path

sgroup.sensor_paths.sensor_path.append(new_sensorpath)

rpc_service = CRUDService()
rpc_service.create(xr, sgroup)

# Subscription

sub = oc_telemetry.TelemetrySystem.Subscriptions.Persistent.Subscription()
sub.subscription_id = 3
sub.config.subscription_id = 3

sub.sensor_profiles = sub.SensorProfiles()

new_sgroup = sub.SensorProfiles.SensorProfile()
new_sgroup.sensor_group = 'SGroup3'
new_sgroup.config.sensor_group = 'SGroup3'
new_sgroup.config.sample_interval = 30000

sub.sensor_profiles.sensor_profile.append(new_sgroup)

rpc_service.create(xr, sub)
