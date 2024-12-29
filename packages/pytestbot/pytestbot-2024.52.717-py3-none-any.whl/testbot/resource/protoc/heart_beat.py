syntax = "proto3";

package testbot.resource.protoc; // 定义包名

import "testbot/resource/protoc/basic_type.proto";

/**
 * 心跳检测grpc服务
 */
service HeartBeat{

  //心跳检测
  rpc checkHeartBeat(Empty) returns (StringType);

}
